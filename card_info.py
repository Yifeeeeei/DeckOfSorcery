"""
用来存储各种属性值
"""


class Elements:
    def __init__(self, elements_dict) -> None:
        self.elements_dict = elements_dict
        all_elements = ["光", "暗", "火", "水", "地", "气", "?"]
        for ele in all_elements:
            if ele not in elements_dict:
                elements_dict[ele] = 0

    def total_cost(self):
        return sum(self.elements_dict.values())

    def __getitem__(self, item):
        return self.elements_dict[item]

    def __setitem__(self, key, value):
        self.elements_dict[key] = value

    def keys(self):
        return self.elements_dict.keys()

    def values(self):
        return self.elements_dict.values()

    def __str__(self) -> str:
        s = ""
        for ele in self.elements_dict.keys():
            if self.elements_dict[ele] > 0:
                s += ele + ":" + str(self.elements_dict[ele]) + " "
        return s


class CardInfo:
    def __init__(self) -> None:
        self.number = 0
        self.type = ""  # 生物、技能、道具、英雄
        self.name = ""
        self.category = ""  # 火水地光暗?

        self.tag = ""  # 说明，传奇异兽、道具、咒术、法术之类的名词
        self.description = ""  # 描述
        self.quote = ""  # 一段帅气的文字引用
        self.elements_cost = Elements({})  # 左上角元素消耗
        self.elements_gain = Elements({})  # 右下角元素负载
        self.attack = -1  # 底部攻击力

        # 以下是生物卡的独有属性

        self.life = -1  # 生命值

        self.version_number = ""  # 版本号
        self.version_name = ""  # 版本名称

        # 以下是技能卡的独有属性
        self.duration = -1  # 冷却回合数
        self.power = -1  # 威力
        self.elements_expense = Elements({})  # 代价（为彩笔？）

        # 衍生物列表
        self.spawns = []

        self.output_path = ""  # 输出图片路径

    def __str__(self):
        s = ""
        s += "编号 " + str(self.number) + "\n"
        s += "类别 " + self.type + "\n"
        s += "名称 " + self.name + "\n"
        s += "元素 " + self.category + "\n"
        s += "标签 " + self.tag + "\n"
        s += "效果 " + self.description + "\n"
        s += "引言 " + self.quote + "\n"
        s += "费用 " + str(self.elements_cost) + "\n"
        s += "负载 " + str(self.elements_gain) + "\n"
        s += "生命 " + str(self.life) + "\n"
        s += "版本 " + str(self.version) + "\n"
        s += "持续 " + str(self.duration) + "\n"
        s += "威力 " + str(self.power) + "\n"
        s += "代价 " + str(self.elements_expense) + "\n"
        s += "衍生 " + str(self.spawns) + "\n"
        return s
