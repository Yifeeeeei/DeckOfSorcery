import pandas as pd
from tqdm import tqdm
import json
import os
from config import *
from card_maker import CardMaker, CardInfo, Elements


class MassProducerXlsx:
    def __init__(self, mass_producer_params_path: str):
        if mass_producer_params_path is None:
            print("No mass_producer_params_path specified!")
            self.all_elements = ["水", "火", "光", "暗", "气", "地", "无"]
            return
        self.mass_producer_params = json.load(
            open(mass_producer_params_path, "r", encoding="utf-8")
        )
        self.mass_producer_params["output_path"] = "output"
        config = None
        if self.mass_producer_params["排版"] == "游戏王":
            config = Config_YuGiOh(self.mass_producer_params["尺寸"])
        if self.mass_producer_params["排版"] == "万智牌":
            config = Config_Magic(self.mass_producer_params["尺寸"])

        self.card_maker_config = config
        self.card_maker_config.general_path = self.mass_producer_params["general_path"]
        self.card_maker_config.font_path = self.mass_producer_params["font_path"]
        self.all_elements = ["水", "火", "光", "暗", "气", "地", "无"]
        self.error_log = []
        self.all_card_infos = []

        self.old_all_card_infos = None
        if "new_cards_only" in self.mass_producer_params and os.path.exists(
            "all_card_infos.json"
        ):
            self.old_all_card_infos = json.load(
                open("all_card_infos.json", "r", encoding="utf-8")
            )

        assert (
            len(self.mass_producer_params["xlsx_paths"])
            == len(self.mass_producer_params["drawing_paths"])
            == len(self.mass_producer_params["version_names"])
        )

    def convert_elements_to_dict(self, elements):
        return elements.elements_dict

    def make_dir(
        self,
        dir_path: str,
    ):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def clean_string(self, s):
        s = s.replace("？", "?")
        s = s.replace("，", ",")
        s = s.replace("。", ".")
        s = s.replace("：", ":")
        s = s.replace("；", ";")
        s = s.replace("！", "!")
        s = s.replace("“", '"')
        s = s.replace("”", '"')
        s = s.replace("‘", "'")
        s = s.replace("’", "'")
        s = s.replace("（", "(")
        s = s.replace("）", ")")
        s = s.replace("【", "[")
        s = s.replace("】", "]")
        return s

    def get_card_type_from_card_number(self, card_number):
        if card_number[0] == "1":
            return "生物"
        if card_number[0] == "2":
            return "道具"
        if card_number[0] == "3":
            return "技能"
        if card_number[0] == "4":
            return "英雄"
        return "未知"

    def element_analysis(self, sentence):
        last_index = -1
        eles = Elements({})
        for i, chi in enumerate(sentence):
            if chi in self.all_elements:
                num = int(sentence[last_index + 1 : i])
                last_index = sentence.index(chi)
                eles[chi] = num
        return eles

    def get_card_info_from_row(self, df_row, version_name=""):
        card_info = CardInfo()
        if "编号" in df_row.keys():
            card_info.number = (
                "" if pd.isnull(df_row["编号"]) else str(int(df_row["编号"]))
            )
        if card_info.number == "":
            return None
        if "属性" in df_row.keys():
            card_info.category = (
                ""
                if pd.isnull(df_row["属性"])
                else self.output_dir_name_to_category(
                    self.clean_string(str(df_row["属性"]).strip())
                )
            )
        if "名称" in df_row.keys():
            card_info.name = (
                ""
                if pd.isnull(df_row["名称"])
                else self.clean_string(str(df_row["名称"]))
            )
        if "标签" in df_row.keys():
            card_info.tag = (
                ""
                if pd.isnull(df_row["标签"])
                else self.clean_string(str(df_row["标签"]))
            )
        if "生命" in df_row.keys():
            card_info.life = int(-1 if pd.isnull(df_row["生命"]) else df_row["生命"])
        if "条件" in df_row.keys():
            card_info.elements_cost = (
                Elements({})
                if pd.isnull(df_row["条件"])
                else self.element_analysis(self.clean_string(df_row["条件"]))
            )
        if "种类" in df_row.keys():
            card_info.tag = str(self.clean_string(df_row["种类"]))
        if "负载" in df_row.keys():
            card_info.elements_gain = (
                Elements({})
                if pd.isnull(df_row["负载"])
                else self.element_analysis(self.clean_string(df_row["负载"]))
            )
        if "效果" in df_row.keys():
            card_info.description = (
                ""
                if pd.isnull(df_row["效果"])
                else str(self.clean_string(df_row["效果"]))
            )
        if "引言" in df_row.keys():
            card_info.quote = (
                ""
                if pd.isnull(df_row["引言"])
                else self.clean_string(str(df_row["引言"]))
            )
        if "威力" in df_row.keys():
            card_info.power = int(-1 if pd.isnull(df_row["威力"]) else df_row["威力"])
        if "时间" in df_row.keys():
            card_info.duration = int(
                -1 if pd.isnull(df_row["时间"]) else df_row["时间"]
            )
        if "代价" in df_row.keys():
            card_info.elements_expense = (
                Elements({})
                if pd.isnull(df_row["代价"])
                else self.element_analysis(df_row["代价"])
            )
        if "攻击" in df_row.keys():
            card_info.attack = int(-1 if pd.isnull(df_row["攻击"]) else df_row["攻击"])
        if "衍生" in df_row.keys():
            if pd.isnull(df_row["衍生"]):
                card_info.spawns = []
            else:
                card_info.spawns = str(df_row["衍生"]).split()
                for i in range(len(card_info.spawns)):
                    card_info.spawns[i] = str(int(float(card_info.spawns[i].strip())))

        if card_info.number == "" or card_info.category == "":
            # 空行
            return None
        # 版本号
        card_info.version_number = card_info.number[3:5]

        # 版本名
        card_info.version_name = version_name

        # 输出路径
        card_info.output_path = self.get_output_path(card_info)

        # 类别
        card_info.type = self.get_card_type_from_card_number(card_info.number)

        return card_info

    def category_to_output_dir_name(self, category):

        return category

    def output_dir_name_to_category(self, output_dir_name):
        return output_dir_name

    def get_output_path(self, card_info):
        return os.path.join(
            self.mass_producer_params["output_path"],
            card_info.version_name,
            card_info.type,
            self.category_to_output_dir_name(card_info.category),
            card_info.number + ".jpg",
        )

    def convert_card_info_to_dict(self, card_info: CardInfo):
        dict = {}
        dict["number"] = card_info.number
        dict["type"] = card_info.type  # 生物、技能、道具三选一
        dict["name"] = card_info.name
        dict["category"] = card_info.category  # 火水地光暗无

        dict["tag"] = card_info.tag  # 说明，传奇异兽、道具、咒术、法术之类的名词
        dict["description"] = card_info.description  # 描述
        dict["quote"] = card_info.quote  # 一段帅气的文字引用
        dict["elements_cost"] = self.convert_elements_to_dict(
            card_info.elements_cost
        )  # 左上角元素消耗
        dict["elements_gain"] = self.convert_elements_to_dict(
            card_info.elements_gain
        )  # 右下角元素负载
        dict["attack"] = card_info.attack  # 底部攻击力

        dict["life"] = card_info.life  # 生命值
        dict["version_number"] = card_info.version_number  # 版本号
        dict["version_name"] = card_info.version_name  # 版本名称

        # 以下是技能卡的独有属性
        dict["duration"] = card_info.duration  # 冷却回合数
        dict["power"] = card_info.power  # 威力
        dict["elements_expense"] = self.convert_elements_to_dict(
            card_info.elements_expense
        )  # 代价（为彩笔？）

        # 衍生物列表
        dict["spawns"] = card_info.spawns

        dict["output_path"] = card_info.output_path  # 输出图片路径
        return dict

    def produce(self):
        number_of_sheets = len(self.mass_producer_params["xlsx_paths"])
        for i in range(number_of_sheets):
            xlsx_path = self.mass_producer_params["xlsx_paths"][i]
            drawing_path = self.mass_producer_params["drawing_paths"][i]
            version_name = self.mass_producer_params["version_names"][i]
            current_sheets = pd.read_excel(
                xlsx_path,
                sheet_name=None,
                header=0,
            )

            card_maker = CardMaker(self.card_maker_config)

            for sheet_name, df in current_sheets.items():
                print(
                    "making cards in",
                    xlsx_path,
                    sheet_name,
                )

                for index, row in tqdm(df.iterrows()):
                    card_info = None
                    try:
                        card_info = self.get_card_info_from_row(row, version_name)
                    except Exception as e:
                        print("Error encountered when parsing row: ", index, row, e)
                        self.error_log.append(str(row) + " " + str(e))
                        continue
                    if card_info is None:
                        continue
                    card_maker.config.drawing_path = drawing_path

                    # should I draw this
                    self.all_card_infos.append(
                        self.convert_card_info_to_dict(card_info)
                    )
                    if (
                        self.old_all_card_infos is not None
                        and self.mass_producer_params["new_cards_only"]
                    ):
                        if self.all_card_infos[
                            -1
                        ] in self.old_all_card_infos and os.path.exists(
                            self.all_card_infos[-1].output_path
                        ):
                            continue

                    try:
                        card_image = None
                        if self.mass_producer_params["打印版"] == False:
                            card_image = card_maker.make_card(card_info).convert("RGB")
                        else:
                            card_image = card_maker.make_card(card_info).convert("CMYK")

                        # create the folders if they don't exist
                        dir = os.path.dirname(card_info.output_path)
                        self.make_dir(dir)
                        card_image.save(
                            card_info.output_path,
                        )

                    except Exception as e:
                        print(
                            "Error encountered when drawing card: ", card_info.name, e
                        )
                        self.all_card_infos.pop()
        # save all_card_infos and generate simplified_card_infos
        if not os.path.exists(self.mass_producer_params["output_path"]):
            os.makedirs(self.mass_producer_params["output_path"])
        all_card_infos_json_path = os.path.join(
            self.mass_producer_params["output_path"], "all_card_infos.json"
        )
        json.dump(
            self.all_card_infos,
            open(all_card_infos_json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
        )
        simplified_card_infos = {}
        for card_info_dict in self.all_card_infos:
            simplified_card_infos[card_info_dict["number"]] = card_info_dict[
                "output_path"
            ]
        simplified_card_infos_json_path = os.path.join(
            self.mass_producer_params["output_path"], "simplified_card_infos.json"
        )
        json.dump(
            simplified_card_infos,
            open(simplified_card_infos_json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
        )
