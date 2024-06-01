"""
配置文件
"""
import os


# base class for config
class Config:
    def __init__(self):
        pass


# default config
# size_ratio大小(1,2,3,4,5...按照比例递增)
class Config_YuGiOh(Config):
    def __init__(self, size_ratio=1):
        super().__init__()
        # 路径
        self.general_path = os.path.join("resources", "general")  # 通用素材
        self.drawing_path = "drawings"  # 卡牌原画
        self.font_path = os.path.join("resources", "fonts")  # 字体

        # 元素图片位置
        self.element_images = {
            "光": "ele_light",
            "暗": "ele_dark",
            "水": "ele_water",
            "火": "ele_fire",
            "气": "ele_air",
            "地": "ele_earth",
            "?": "ele_none",
        }
        self.element_back = {
            "光": "back_light",
            "暗": "back_dark",
            "水": "back_water",
            "火": "back_fire",
            "气": "back_air",
            "地": "back_earth",
            "?": "back_none",
        }
        # 卡片
        self.card_width = int(590 * size_ratio)
        self.card_height = int(860 * size_ratio)
        # 卡片原画
        self.drawing_width = int(540 * size_ratio)
        self.drawing_height = int(540 * size_ratio)  # 530 ok,
        self.drawing_to_upper = int(35 * size_ratio)
        # 卡片边框
        self.border_width = int(580 * size_ratio)
        self.border_height = int(830 * size_ratio)
        self.type_border = {"生物": "border", "技能": "border4", "道具": "border3"}
        # 英雄牌
        self.reverse_color_for_hero = True
        # 底部的白色块
        self.bottom_block_width = int(540 * size_ratio)
        self.bottom_block_height = int(260 * size_ratio)
        self.bottom_block_color = (255, 255, 255)
        self.bottom_block_transparency = 150
        self.bottom_block_legend_radius = int(0 * size_ratio)
        # 左上元素+名称
        self.name_font_size = int(40 * size_ratio)
        self.name_font = "MaShanZheng-Regular.ttf"
        self.name_rect_height = int(60 * size_ratio)
        self.name_rect_left = int(60 * size_ratio)
        self.name_rect_top = int(10 * size_ratio)
        self.name_rect_radius = int(10 * size_ratio)
        self.name_rect_fill = (255, 195, 0)
        self.name_text_to_left = int(90 * size_ratio)
        self.name_text_left_compensation = 5
        self.name_rect_outline_color = (255, 255, 255)
        self.name_rect_outline_width = int(3 * size_ratio)
        self.name_text_font_color = (0, 0, 0)
        self.name_category_width = int(80 * size_ratio)
        self.name_category_left = int(5 * size_ratio)
        self.name_category_top = int(5 * size_ratio)
        # 中央消耗
        self.cost_font_size = int(30 * size_ratio)
        self.cost_font = "ShareTechMono-Regular.ttf"
        self.cost_category_width = int(30 * size_ratio)
        self.cost_font_compensation = 2
        self.cost_font_color = (0, 0, 0)
        self.cost_padding = int(5 * size_ratio)
        self.cost_rect_top = int(530 * size_ratio)
        self.cost_rect_left = int(10 * size_ratio)
        self.cost_rect_height = int(50 * size_ratio)
        self.cost_rect_radius = int(25 * size_ratio)
        self.cost_rect_fill = (255, 195, 0)
        self.cost_rect_outline_color = (255, 255, 255)
        self.cost_rect_outline_width = int(3 * size_ratio)
        # 中央代价
        self.expense_font_size = int(30 * size_ratio)
        self.expense_font = "ShareTechMono-Regular.ttf"
        self.expense_category_width = int(30 * size_ratio)
        self.expense_font_compensation = 2
        self.expense_font_color = (0, 0, 0)
        self.expense_padding = int(5 * size_ratio)
        self.expense_rect_top = int(530 * size_ratio)
        self.expense_rect_right = int(580 * size_ratio)
        self.expense_rect_height = int(50 * size_ratio)
        self.expense_rect_radius = int(25 * size_ratio)
        self.expense_rect_fill = (255, 195, 0)
        self.expense_rect_outline_color = (255, 255, 255)
        self.expense_rect_outline_width = int(3 * size_ratio)
        # 标签
        self.tag_font = "FangZhengKaiTiJianTi-1.ttf"
        self.tag_font_size = int(24 * size_ratio)
        self.tag_font_color = (0, 0, 0)
        self.tag_text_left = int(50 * size_ratio)
        self.tag_text_to_block_top = int(15 * size_ratio)
        # 卡牌描述
        self.discription_font = "FangZhengKaiTiJianTi-1.ttf"
        self.discription_font_size = int(24 * size_ratio)
        self.discription_font_color = (0, 0, 0)
        self.discription_text_left = int(50 * size_ratio)
        self.discription_text_to_block_top = int(55 * size_ratio)
        self.discription_line_spacing = int(10 * size_ratio)
        # 卡牌引言
        self.quote_font = "FangZhengKaiTiJianTi-1.ttf"
        self.quote_font_size = int(20 * size_ratio)
        self.quote_font_color = (32, 32, 32)
        self.quote_text_left = int(100 * size_ratio)
        self.quote_text_to_block_bottom = int(40 * size_ratio)
        self.quote_line_spacing = int(5 * size_ratio)
        # 底部负载
        self.gain_font_size = int(30 * size_ratio)
        self.gain_font = "ShareTechMono-Regular.ttf"
        self.gain_category_width = int(30 * size_ratio)
        self.gain_font_compensation = 1
        self.gain_font_color = (0, 0, 0)
        self.gain_padding = int(5 * size_ratio)
        self.gain_rect_top = int(800 * size_ratio)
        self.gain_rect_right = int(580 * size_ratio)
        self.gain_rect_height = int(50 * size_ratio)
        self.gain_rect_radius = int(25 * size_ratio)
        self.gain_rect_fill = (255, 195, 0)
        self.gain_rect_outline_color = (255, 255, 255)
        self.gain_rect_outline_width = int(3 * size_ratio)
        # 底部生命
        self.life_font_size = int(30 * size_ratio)
        self.life_font = "ShareTechMono-Regular.ttf"
        self.life_icon_width = int(30 * size_ratio)
        self.life_font_compensation = 2
        self.life_font_color = (0, 0, 0)
        self.life_padding = int(5 * size_ratio)
        self.life_rect_top = int(800 * size_ratio)
        self.life_rect_left = int(10 * size_ratio)
        self.life_rect_height = int(50 * size_ratio)
        self.life_rect_radius = int(25 * size_ratio)
        self.life_rect_fill = (255, 195, 0)
        self.life_rect_outline_color = (255, 255, 255)
        self.life_rect_outline_width = int(3 * size_ratio)
        # 底部攻击
        self.attack_font_size = int(30 * size_ratio)
        self.attack_font = "ShareTechMono-Regular.ttf"
        self.attack_icon_width = int(30 * size_ratio)
        self.attack_font_compensation = 2
        self.attack_font_color = (0, 0, 0)
        self.attack_padding = int(5 * size_ratio)
        self.attack_rect_top = int(800 * size_ratio)
        # self.life_rect_left = ??? we will calculate this in the process
        self.attack_rect_height = int(50 * size_ratio)
        self.attack_rect_radius = int(25 * size_ratio)
        self.attack_rect_fill = (255, 195, 0)
        self.attack_rect_outline_color = (255, 255, 255)
        self.attack_rect_outline_width = int(3 * size_ratio)
        # 底部威力或持续时间
        self.power_or_duration_font_size = int(30 * size_ratio)
        self.power_or_duration_font = "ShareTechMono-Regular.ttf"
        self.power_or_duration_icon_width = int(30 * size_ratio)
        self.power_or_duration_font_compensation = 2
        self.power_or_duration_font_color = (0, 0, 0)
        self.power_or_duration_padding = int(5 * size_ratio)
        self.power_or_duration_rect_top = int(800 * size_ratio)
        self.power_or_duration_rect_right = int(580 * size_ratio)
        self.power_or_duration_rect_height = int(50 * size_ratio)
        self.power_or_duration_rect_radius = int(25 * size_ratio)
        self.power_or_duration_rect_fill = (255, 195, 0)
        self.power_or_duration_rect_outline_color = (255, 255, 255)
        self.power_or_duration_rect_outline_width = int(3 * size_ratio)
        # 绘制卡牌编号
        self.number_font_size = int(20 * size_ratio)
        self.number_font_color = (0, 0, 0)
        self.number_text_to_right = int(50 * size_ratio)
        self.number_text_to_block_top = int(17 * size_ratio)
        self.number_font = "ShareTechMono-Regular.ttf"


class Config_Magic(Config):
    def __init__(self, size_ratio=1):
        super().__init__()
        # 路径
        self.general_path = os.path.join("resources", "general")  # 通用素材
        self.drawing_path = "drawings"  # 卡牌原画
        self.font_path = os.path.join("resources", "fonts")  # 字体

        # 元素图片位置
        self.element_images = {
            "光": "ele_light",
            "暗": "ele_dark",
            "水": "ele_water",
            "火": "ele_fire",
            "气": "ele_air",
            "地": "ele_earth",
            "?": "ele_none",
        }
        self.element_back = {
            "光": "back_light",
            "暗": "back_dark",
            "水": "back_water",
            "火": "back_fire",
            "气": "back_air",
            "地": "back_earth",
            "?": "back_none",
        }
        # 卡片
        self.card_width = int(630 * size_ratio)
        self.card_height = int(880 * size_ratio)
        # 卡片原画
        self.drawing_width = int(540 * size_ratio)
        self.drawing_height = int(540 * size_ratio)  # 530 ok,
        self.drawing_to_upper = int(30 * size_ratio)
        # 卡片边框
        self.border_width = int(600 * size_ratio)
        self.border_height = int(860 * size_ratio)
        self.type_border = {"生物": "border", "技能": "border4", "道具": "border3"}
        # 英雄牌
        self.reverse_color_for_hero = True
        # 底部的白色块
        self.bottom_block_width = int(540 * size_ratio)
        self.bottom_block_height = int(280 * size_ratio)
        self.bottom_block_color = (255, 255, 255)
        self.bottom_block_transparency = 150
        self.bottom_block_legend_radius = int(0 * size_ratio)
        # 左上元素+名称
        self.name_font_size = int(40 * size_ratio)
        self.name_font = "MaShanZheng-Regular.ttf"
        self.name_rect_height = int(60 * size_ratio)
        self.name_rect_left = int(60 * size_ratio)
        self.name_rect_top = int(10 * size_ratio)
        self.name_rect_radius = int(10 * size_ratio)
        self.name_rect_fill = (255, 195, 0)
        self.name_text_to_left = int(90 * size_ratio)
        self.name_text_left_compensation = 5
        self.name_rect_outline_color = (255, 255, 255)
        self.name_rect_outline_width = int(3 * size_ratio)
        self.name_text_font_color = (0, 0, 0)
        self.name_category_width = int(80 * size_ratio)
        self.name_category_left = int(5 * size_ratio)
        self.name_category_top = int(5 * size_ratio)
        # 中央消耗
        self.cost_font_size = int(30 * size_ratio)
        self.cost_font = "ShareTechMono-Regular.ttf"
        self.cost_category_width = int(30 * size_ratio)
        self.cost_font_compensation = 2
        self.cost_font_color = (0, 0, 0)
        self.cost_padding = int(5 * size_ratio)
        self.cost_rect_top = int(530 * size_ratio)
        self.cost_rect_left = int(10 * size_ratio)
        self.cost_rect_height = int(50 * size_ratio)
        self.cost_rect_radius = int(25 * size_ratio)
        self.cost_rect_fill = (255, 195, 0)
        self.cost_rect_outline_color = (255, 255, 255)
        self.cost_rect_outline_width = int(3 * size_ratio)
        # 中央代价
        self.expense_font_size = int(30 * size_ratio)
        self.expense_font = "ShareTechMono-Regular.ttf"
        self.expense_category_width = int(30 * size_ratio)
        self.expense_font_compensation = 2
        self.expense_font_color = (0, 0, 0)
        self.expense_padding = int(5 * size_ratio)
        self.expense_rect_top = int(530 * size_ratio)
        self.expense_rect_right = int(620 * size_ratio)
        self.expense_rect_height = int(50 * size_ratio)
        self.expense_rect_radius = int(25 * size_ratio)
        self.expense_rect_fill = (255, 195, 0)
        self.expense_rect_outline_color = (255, 255, 255)
        self.expense_rect_outline_width = int(3 * size_ratio)
        # 标签
        self.tag_font = "FangZhengKaiTiJianTi-1.ttf"
        self.tag_font_size = int(24 * size_ratio)
        self.tag_font_color = (0, 0, 0)
        self.tag_text_left = int(50 * size_ratio)
        self.tag_text_to_block_top = int(15 * size_ratio)
        # 卡牌描述
        self.discription_font = "FangZhengKaiTiJianTi-1.ttf"
        self.discription_font_size = int(24 * size_ratio)
        self.discription_font_color = (0, 0, 0)
        self.discription_text_left = int(50 * size_ratio)
        self.discription_text_to_block_top = int(55 * size_ratio)
        self.discription_line_spacing = int(10 * size_ratio)
        # 卡牌引言
        self.quote_font = "FangZhengKaiTiJianTi-1.ttf"
        self.quote_font_size = int(20 * size_ratio)
        self.quote_font_color = (32, 32, 32)
        self.quote_text_left = int(100 * size_ratio)
        self.quote_text_to_block_bottom = int(40 * size_ratio)
        self.quote_line_spacing = int(5 * size_ratio)
        # 底部负载
        self.gain_font_size = int(30 * size_ratio)
        self.gain_font = "ShareTechMono-Regular.ttf"
        self.gain_category_width = int(30 * size_ratio)
        self.gain_font_compensation = 1
        self.gain_font_color = (0, 0, 0)
        self.gain_padding = int(5 * size_ratio)
        self.gain_rect_top = int(820 * size_ratio)
        self.gain_rect_right = int(620 * size_ratio)
        self.gain_rect_height = int(50 * size_ratio)
        self.gain_rect_radius = int(25 * size_ratio)
        self.gain_rect_fill = (255, 195, 0)
        self.gain_rect_outline_color = (255, 255, 255)
        self.gain_rect_outline_width = int(3 * size_ratio)
        # 中央代价
        self.expense_font_size = int(30 * size_ratio)
        self.expense_font = "ShareTechMono-Regular.ttf"
        self.expense_category_width = int(30 * size_ratio)
        self.expense_font_compensation = 2
        self.expense_font_color = (0, 0, 0)
        self.expense_padding = int(5 * size_ratio)
        self.expense_rect_top = int(530 * size_ratio)
        self.expense_rect_right = int(580 * size_ratio)
        self.expense_rect_height = int(50 * size_ratio)
        self.expense_rect_radius = int(25 * size_ratio)
        self.expense_rect_fill = (255, 195, 0)
        self.expense_rect_outline_color = (255, 255, 255)
        self.expense_rect_outline_width = int(3 * size_ratio)
        # 底部生命
        self.life_font_size = int(30 * size_ratio)
        self.life_font = "ShareTechMono-Regular.ttf"
        self.life_icon_width = int(30 * size_ratio)
        self.life_font_compensation = 2
        self.life_font_color = (0, 0, 0)
        self.life_padding = int(5 * size_ratio)
        self.life_rect_top = int(820 * size_ratio)
        self.life_rect_left = int(10 * size_ratio)
        self.life_rect_height = int(50 * size_ratio)
        self.life_rect_radius = int(25 * size_ratio)
        self.life_rect_fill = (255, 195, 0)
        self.life_rect_outline_color = (255, 255, 255)
        self.life_rect_outline_width = int(3 * size_ratio)
        # 底部攻击
        self.attack_font_size = int(30 * size_ratio)
        self.attack_font = "ShareTechMono-Regular.ttf"
        self.attack_icon_width = int(30 * size_ratio)
        self.attack_font_compensation = 2
        self.attack_font_color = (0, 0, 0)
        self.attack_padding = int(5 * size_ratio)
        self.attack_rect_top = int(800 * size_ratio)
        # self.life_rect_left = ??? we will calculate this in the process
        self.attack_rect_height = int(50 * size_ratio)
        self.attack_rect_radius = int(25 * size_ratio)
        self.attack_rect_fill = (255, 195, 0)
        self.attack_rect_outline_color = (255, 255, 255)
        self.attack_rect_outline_width = int(3 * size_ratio)
        # 底部威力或持续时间
        self.power_or_duration_font_size = int(30 * size_ratio)
        self.power_or_duration_font = "ShareTechMono-Regular.ttf"
        self.power_or_duration_icon_width = int(30 * size_ratio)
        self.power_or_duration_font_compensation = 2
        self.power_or_duration_font_color = (0, 0, 0)
        self.power_or_duration_padding = int(5 * size_ratio)
        self.power_or_duration_rect_top = int(820 * size_ratio)
        self.power_or_duration_rect_right = int(620 * size_ratio)
        self.power_or_duration_rect_height = int(50 * size_ratio)
        self.power_or_duration_rect_radius = int(25 * size_ratio)
        self.power_or_duration_rect_fill = (255, 195, 0)
        self.power_or_duration_rect_outline_color = (255, 255, 255)
        self.power_or_duration_rect_outline_width = int(3 * size_ratio)
        # 绘制卡牌编号
        self.number_font_size = int(20 * size_ratio)
        self.number_font_color = (0, 0, 0)
        self.number_text_to_right = int(50 * size_ratio)
        self.number_text_to_block_top = int(17 * size_ratio)
        self.number_font = "ShareTechMono-Regular.ttf"
