import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import textwrap
import os

from config import Config

from card_info import Elements, CardInfo


"""
卡牌制作类
"""


class CardMaker:
    def __init__(self, config: Config) -> None:
        self.config = config

    def translator(self, chi):
        if chi == "光":
            return "light"
        elif chi == "暗":
            return "dark"
        elif chi == "火":
            return "fire"
        elif chi == "水":
            return "water"
        elif chi == "气":
            return "air"
        elif chi == "地":
            return "earth"
        elif chi == "?" or chi == "无" or chi == "？":
            return "none"
        else:
            print("invalid chi encounterd: " + chi)
            return None

    def adjust_image(self, image, target_width_and_height):
        width, height = image.size
        target_width, target_height = target_width_and_height
        if (width / height) > (target_width / target_height):
            # too wide
            ideal_width = target_width / target_height * height
            left = (width - ideal_width) / 2
            right = (width + ideal_width) / 2
            image = image.crop((left, 0, right, height))
        if (width / height) < (target_width / target_height):
            # too tall
            ideal_height = target_height / target_width * width
            top = (height - ideal_height) / 2
            bottom = (height + ideal_height) / 2
            image = image.crop((0, top, width, bottom))
        image = image.resize((target_width, target_height))
        return image

    def get_image_without_extension(self, image_name):
        extension_list = [".png", ".jpg", ".webp", ".jpeg", ".jfif"]
        for ext in extension_list:
            if os.path.exists(image_name + ext):
                return PIL.Image.open(image_name + ext).convert("RGBA")
        print("could not find image: " + image_name)
        return None

    def get_drawing(self, card_info: CardInfo):
        return self.get_image_without_extension(
            os.path.join(self.config.drawing_path, str(card_info.number))
        )

    def get_background(self, card_info: CardInfo):
        bg_image = self.get_image_without_extension(
            os.path.join(
                self.config.general_path, self.config.element_back[card_info.category]
            )
        )
        bg_image = self.adjust_image(
            bg_image, (self.config.card_width, self.config.card_height)
        )
        return bg_image

    def get_border(self, card_info: CardInfo):
        border_image = self.get_image_without_extension(
            os.path.join(
                self.config.general_path, self.config.type_border[card_info.type]
            )
        )
        border_image = self.adjust_image(
            border_image, (self.config.border_width, self.config.border_height)
        )
        return border_image

    def reverse_color(self, color):
        return (255 - color[0], 255 - color[1], 255 - color[2])

    def draw_bottom_block(self, base_image, card_info: CardInfo):
        if not self.is_legend(card_info):
            new_image = PIL.Image.new("RGBA", base_image.size, (255, 255, 255, 0))
            draw = PIL.ImageDraw.Draw(new_image)
            top = self.config.drawing_to_upper + self.config.drawing_height
            left = (self.config.card_width - self.config.bottom_block_width) / 2
            bottom = (
                self.config.drawing_to_upper
                + self.config.drawing_height
                + self.config.bottom_block_height
            )
            right = left + self.config.bottom_block_width

            color = self.config.bottom_block_color
            if self.config.reverse_color_for_hero and card_info.type == "英雄":
                color = self.reverse_color(color)

            draw.rectangle(
                ((left, top), (right, bottom)),
                fill=color + (self.config.bottom_block_transparency,),
            )
            out = PIL.Image.alpha_composite(base_image, new_image)
            return out
        else:
            new_image = PIL.Image.new("RGBA", base_image.size, (255, 255, 255, 0))
            draw = PIL.ImageDraw.Draw(new_image)
            top = self.config.drawing_to_upper + self.config.drawing_height
            left = (self.config.card_width - self.config.bottom_block_width) / 2
            bottom = (
                self.config.drawing_to_upper
                + self.config.drawing_height
                + self.config.bottom_block_height
            )
            right = left + self.config.bottom_block_width
            color = self.config.bottom_block_color
            if self.config.reverse_color_for_hero and card_info.type == "英雄":
                color = self.reverse_color(color)

            draw.rounded_rectangle(
                ((left, top), (right, bottom)),
                self.config.bottom_block_legend_radius,
                fill=color + (self.config.bottom_block_transparency,),
            )
            out = PIL.Image.alpha_composite(base_image, new_image)
            return out

    def is_legend(self, card_info: CardInfo):
        if (
            "传说" in card_info.tag
            or "传奇" in card_info.tag
            or card_info.type == "英雄"
        ):
            return True
        return False

    # 准备好底板，除了描述和血量，元素消耗之类的其他东西，包括原画
    def prepare_outline(self, card_info: CardInfo):
        if not self.is_legend(card_info):
            # 添加背景
            base_image = self.get_background(card_info)
            # 添加卡牌原画
            drawing_image = self.get_drawing(card_info)
            base_image = self.adjust_image(
                base_image, (self.config.card_width, self.config.card_height)
            )
            drawing_image = self.adjust_image(
                drawing_image, (self.config.drawing_width, self.config.drawing_height)
            )
            # 添加原画
            base_image.paste(
                drawing_image,
                (
                    int((self.config.card_width - self.config.drawing_width) / 2),
                    self.config.drawing_to_upper,
                ),
            )
            # 添加底部文字背景
            base_image = self.draw_bottom_block(base_image, card_info)

            # 获取边框
            border_image = self.get_border(card_info)
            # 添加边框
            base_image.paste(
                border_image,
                (
                    int((self.config.card_width - self.config.border_width) / 2),
                    int((self.config.card_height - self.config.border_height) / 2),
                ),
                mask=border_image,
            )

            return base_image
        else:
            base_image = self.get_drawing(card_info)
            # 添加卡牌原画
            base_image = self.adjust_image(
                base_image, (self.config.card_width, self.config.card_height)
            )
            base_image = self.draw_bottom_block(base_image, card_info)

            return base_image

    def estimate_text_size(self, text, font):
        length = font.getsize(text)[0]
        return length

    def draw_round_corner_rectangle(
        self, image, left_top_right_bottom, radius, color, outline=None, width=1
    ):
        """Draws a round corner rectangle on the given image.

        Args:
            image: The image to draw the rectangle on.
            top_left: The top-left corner of the rectangle.
            bottom_right: The bottom-right corner of the rectangle.
            radius: The radius of the corners.
            color: The color of the rectangle.
            outline: The color of the outline of the rectangle.
            width: The width of the outline of the rectangle.

        Returns:
            The image with the rectangle drawn on it.
        """

        # Create a drawing context for the image.
        draw = PIL.ImageDraw.Draw(image)

        # Draw the rectangle on the image.
        draw.rounded_rectangle(
            left_top_right_bottom, radius, fill=color, outline=outline, width=width
        )

        return image

    def add_text_on_image(self, image, text, left_top, font, color, features=None):
        draw = PIL.ImageDraw.Draw(image)
        draw.text(left_top, text, font=font, fill=color, features=features)
        return image

    def get_category_image(self, category: str):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, self.config.element_images[category])
        )

    def draw_category_and_name(self, card_info: CardInfo, base_image: PIL.Image):
        # add name
        text_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.name_font),
            self.config.name_font_size,
        )
        length_estimate = self.estimate_text_size(card_info.name, text_font)
        rectangle_width = length_estimate + 2 * (
            self.config.name_text_to_left - self.config.name_rect_left
        )
        left = self.config.name_rect_left
        top = self.config.name_rect_top
        right = left + rectangle_width
        bottom = top + self.config.name_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (left, top, right, bottom),
            self.config.name_rect_radius,
            self.config.name_rect_fill,
            self.config.name_rect_outline_color,
            self.config.name_rect_outline_width,
        )
        text_left = (
            self.config.name_text_to_left + self.config.name_text_left_compensation
        )
        text_height = text_font.getsize(card_info.name)[1]
        text_top = (
            self.config.name_rect_top + (self.config.name_rect_height - text_height) / 2
        )

        base_image = self.add_text_on_image(
            base_image,
            card_info.name,
            (text_left, text_top),
            text_font,
            self.config.name_text_font_color,
        )

        # add category

        category_image = self.get_category_image(card_info.category)
        category_image = self.adjust_image(
            category_image,
            (
                self.config.name_category_width,
                self.config.name_category_width,
            ),
        )
        base_image.paste(
            category_image,
            (self.config.name_category_left, self.config.name_category_top),
            mask=category_image,
        )

        return base_image

    def draw_cost(self, card_info: CardInfo, base_image: PIL.Image):
        # estimate the length
        all_costs = []
        for ele in card_info.elements_cost.keys():
            if card_info.elements_cost[ele] > 0:
                all_costs.append((ele, card_info.elements_cost[ele]))
        # nothing to do here
        if len(all_costs) == 0:
            return base_image

        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.cost_font),
            self.config.cost_font_size,
        )

        number_length = 0
        for tup in all_costs:
            number_length += font.getsize(str(tup[1]))[0]
        category_length = len(all_costs) * self.config.cost_category_width
        total_length = (
            number_length
            + category_length
            + len(all_costs) * self.config.cost_padding * 2
            + self.config.cost_padding
        )
        # draw the rectangle
        rect_top = self.config.cost_rect_top
        rect_left = self.config.cost_rect_left
        rect_right = rect_left + total_length
        rect_bottom = rect_top + self.config.cost_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (rect_left, rect_top, rect_right, rect_bottom),
            self.config.cost_rect_radius,
            self.config.cost_rect_fill,
            self.config.cost_rect_outline_color,
            self.config.cost_rect_outline_width,
        )
        # put in the numbers and categories
        left_pointer = rect_left + self.config.cost_padding
        text_height = font.getsize("1")[1]
        text_top = int(
            rect_top
            + (self.config.cost_rect_height - text_height) / 2
            - self.config.cost_font_compensation
        )
        category_top = int(
            rect_top
            + (self.config.cost_rect_height - self.config.cost_category_width) / 2
        )
        # sort all costs, put the corresponding element to the head
        for tup in all_costs:
            if tup[0] == card_info.category:
                all_costs.remove(tup)
                all_costs.insert(0, tup)
                break
        # draw the elements
        for tup in all_costs:
            # draw the number
            base_image = self.add_text_on_image(
                base_image,
                str(tup[1]),
                (left_pointer, text_top),
                font,
                self.config.cost_font_color,
            )
            left_pointer += font.getsize(str(tup[1]))[0] + self.config.cost_padding

            # draw the category
            category_image = self.get_category_image(tup[0])
            category_image = self.adjust_image(
                category_image,
                (
                    self.config.cost_category_width,
                    self.config.cost_category_width,
                ),
            )
            base_image.paste(
                category_image,
                (left_pointer, category_top),
                mask=category_image,
            )
            left_pointer += self.config.cost_category_width + self.config.cost_padding

        return base_image

    def draw_tag(self, card_info: CardInfo, base_image: PIL.Image):
        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.tag_font),
            self.config.tag_font_size,
        )
        color = self.config.tag_font_color
        if self.config.reverse_color_for_hero and card_info.type == "英雄":
            color = self.reverse_color(color)
        base_image = self.add_text_on_image(
            base_image,
            card_info.tag,
            (
                self.config.tag_text_left,
                self.config.tag_text_to_block_top
                + self.config.drawing_to_upper
                + self.config.drawing_height,
            ),
            font,
            color,
        )
        return base_image

    def draw_discription_and_quote(self, card_info: CardInfo, base_image: PIL.Image):
        # dynamically adjust font size
        discription_font_size = self.config.tag_font_size
        quote_font_size = self.config.quote_font_size
        discription_line_spacing = self.config.discription_line_spacing
        quote_line_spacing = self.config.quote_line_spacing
        discription_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.discription_font),
            discription_font_size,
        )

        quote_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.quote_font),
            quote_font_size,
        )

        estimated_total_height = 0

        # estimate discription height

        discription_textwrap_width_pixel = (
            self.config.card_width - self.config.discription_text_left * 2
        )
        discription_textwrap_width = int(
            discription_textwrap_width_pixel / discription_font.getsize("标")[0]
        )
        discription_wrapped_text = textwrap.wrap(
            card_info.description, width=discription_textwrap_width
        )
        discription_text_height = discription_font.getsize("标")[1]
        discription_height = discription_line_spacing + (
            discription_text_height + discription_line_spacing
        ) * len(discription_wrapped_text)

        # estimate quote height
        quote_textwrap_width_pixel = (
            self.config.card_width - self.config.quote_text_left * 2
        )
        quote_textwrap_width = int(
            quote_textwrap_width_pixel / quote_font.getsize("标")[0]
        )
        quote_wrapped_text = textwrap.wrap(card_info.quote, width=quote_textwrap_width)
        quote_text_height = quote_font.getsize("标")[1]
        quote_height = quote_line_spacing + (
            quote_text_height + quote_line_spacing
        ) * len(quote_wrapped_text)
        estimated_total_height = discription_height + quote_height

        while (
            estimated_total_height
            > self.config.bottom_block_height
            - self.config.discription_text_to_block_top
            - self.config.quote_text_to_block_bottom
        ):
            alpha = 0.9
            discription_font_size = int(discription_font_size * alpha)
            quote_font_size = int(quote_font_size * alpha)
            discription_line_spacing = int(discription_line_spacing * alpha)
            quote_line_spacing = int(quote_line_spacing * alpha)
            discription_font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.discription_font),
                discription_font_size,
            )

            quote_font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.quote_font),
                quote_font_size,
            )

            # estimate discription height

            discription_textwrap_width_pixel = (
                self.config.card_width - self.config.discription_text_left * 2
            )
            discription_textwrap_width = int(
                discription_textwrap_width_pixel / discription_font.getsize("标")[0]
            )
            discription_wrapped_text = textwrap.wrap(
                card_info.description, width=discription_textwrap_width
            )
            discription_text_height = discription_font.getsize("标")[1]
            discription_height = discription_line_spacing + (
                discription_text_height + discription_line_spacing
            ) * len(discription_wrapped_text)

            # estimate quote height
            quote_textwrap_width_pixel = (
                self.config.card_width - self.config.quote_text_left * 2
            )
            quote_textwrap_width = int(
                quote_textwrap_width_pixel / quote_font.getsize("标")[0]
            )
            quote_wrapped_text = textwrap.wrap(
                card_info.quote, width=quote_textwrap_width
            )
            quote_text_height = quote_font.getsize("标")[1]
            quote_height = quote_line_spacing + (
                quote_text_height + quote_line_spacing
            ) * len(quote_wrapped_text)
            estimated_total_height = discription_height + quote_height

        # start drawing
        # draw discription
        discription_top_pointer = (
            self.config.discription_text_to_block_top
            + self.config.drawing_to_upper
            + self.config.drawing_height
        )
        discription_color = self.config.discription_font_color
        if self.config.reverse_color_for_hero and card_info.type == "英雄":
            discription_color = self.reverse_color(discription_color)

        for line in discription_wrapped_text:
            base_image = self.add_text_on_image(
                base_image,
                line,
                (
                    self.config.discription_text_left,
                    discription_top_pointer,
                ),
                discription_font,
                discription_color,
            )
            discription_top_pointer += (
                discription_line_spacing + discription_text_height
            )
        # draw quote
        quote_bottom_pointer = (
            self.config.bottom_block_height
            + self.config.drawing_to_upper
            + self.config.drawing_height
            - self.config.quote_text_to_block_bottom
            - quote_text_height
        )
        quote_color = self.config.quote_font_color
        if self.config.reverse_color_for_hero and card_info.type == "英雄":
            quote_color = self.reverse_color(quote_color)

        for line in reversed(quote_wrapped_text):
            base_image = self.add_text_on_image(
                base_image,
                line,
                (
                    (self.config.card_width - quote_font.getsize(line)[0]) / 2,
                    quote_bottom_pointer,
                ),
                quote_font,
                quote_color,
            )
            quote_bottom_pointer -= quote_line_spacing + quote_text_height
        return base_image

    def draw_gain(self, card_info: CardInfo, base_image: PIL.Image):
        # estimate the length
        all_gains = []
        for ele in card_info.elements_gain.keys():
            if card_info.elements_gain[ele] > 0:
                all_gains.append((ele, card_info.elements_gain[ele]))
        # nothing to do here
        if len(all_gains) == 0:
            return base_image

        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.gain_font),
            self.config.gain_font_size,
        )

        number_length = 0
        for tup in all_gains:
            number_length += font.getsize(str(tup[1]))[0]
        category_length = len(all_gains) * self.config.gain_category_width
        total_length = (
            number_length
            + category_length
            + len(all_gains) * self.config.gain_padding * 2
            + self.config.gain_padding
        )
        # draw the rectangle
        rect_top = self.config.gain_rect_top
        rect_right = self.config.gain_rect_right
        rect_left = rect_right - total_length
        rect_bottom = rect_top + self.config.gain_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (rect_left, rect_top, rect_right, rect_bottom),
            self.config.gain_rect_radius,
            self.config.gain_rect_fill,
            self.config.gain_rect_outline_color,
            self.config.gain_rect_outline_width,
        )
        # put in the numbers and categories
        text_height = font.getsize("8")[1]
        right_pointer = (
            rect_right - self.config.gain_padding - self.config.gain_category_width
        )

        text_top = int(
            rect_top
            + (self.config.gain_rect_height - text_height) / 2
            - self.config.gain_font_compensation
        )
        category_top = int(
            rect_top
            + (self.config.gain_rect_height - self.config.gain_category_width) / 2
        )
        # sort all gains, put the corresponding element to the head
        for tup in all_gains:
            if tup[0] == card_info.category:
                all_gains.remove(tup)
                all_gains.insert(0, tup)
                break
        all_gains = reversed(all_gains)
        # draw the elements
        for tup in all_gains:
            # draw the category
            category_image = self.get_category_image(tup[0])
            category_image = self.adjust_image(
                category_image,
                (
                    self.config.gain_category_width,
                    self.config.gain_category_width,
                ),
            )
            base_image.paste(
                category_image,
                (right_pointer, category_top),
                mask=category_image,
            )
            right_pointer -= font.getsize(str(tup[1]))[0] + self.config.gain_padding

            # draw the number
            base_image = self.add_text_on_image(
                base_image,
                str(tup[1]),
                (right_pointer, text_top),
                font,
                self.config.gain_font_color,
            )
            right_pointer -= self.config.gain_category_width + self.config.gain_padding

        return base_image

    def get_attack_image(self):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "attack")
        )

    def get_life_image(self):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "life")
        )

    def draw_life_and_attack(self, card_info: CardInfo, base_image: PIL.Image):
        left_pointer = 0
        if card_info.life < 0:
            pass
        else:
            life_image = self.get_life_image()
            life_image = self.adjust_image(
                life_image, (self.config.life_icon_width, self.config.life_icon_width)
            )
            font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.life_font),
                self.config.life_font_size,
            )
            estimated_length = (
                font.getsize(str(card_info.life))[0]
                + self.config.life_padding * 3
                + self.config.life_icon_width
            )
            left = self.config.life_rect_left
            top = self.config.life_rect_top
            right = left + estimated_length
            bottom = top + self.config.life_rect_height
            base_image = self.draw_round_corner_rectangle(
                base_image,
                (left, top, right, bottom),
                self.config.life_rect_radius,
                self.config.life_rect_fill,
                self.config.life_rect_outline_color,
                self.config.life_rect_outline_width,
            )

            left_pointer = left + self.config.life_padding
            life_top = int(
                self.config.life_rect_top
                + (self.config.life_rect_height - self.config.life_icon_width) / 2
            )
            base_image.paste(
                life_image,
                (left_pointer, life_top),
                mask=life_image,
            )
            left_pointer += self.config.life_icon_width + self.config.life_padding
            life_text_top = int(
                self.config.life_rect_top
                + (self.config.life_rect_height - font.getsize(str(card_info.life))[1])
                / 2
                - self.config.life_font_compensation
            )
            base_image = self.add_text_on_image(
                base_image,
                str(card_info.life),
                (left_pointer, life_text_top),
                font,
                self.config.life_font_color,
            )
            # return base_image

        if card_info.attack < 0:
            pass
        else:
            attack_image = self.get_attack_image()
            attack_image = self.adjust_image(
                attack_image,
                (self.config.attack_icon_width, self.config.attack_icon_width),
            )
            font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.attack_font),
                self.config.attack_font_size,
            )
            estimated_length = (
                font.getsize(str(card_info.attack))[0]
                + self.config.attack_padding * 3
                + self.config.attack_icon_width
            )
            # adjust left pointer
            if card_info.life == 0:
                left_pointer = self.config.life_rect_left
            else:
                left_pointer += (
                    self.config.life_rect_left + 3 * self.config.life_padding
                )

            left = left_pointer
            top = self.config.attack_rect_top
            right = left + estimated_length
            bottom = top + self.config.attack_rect_height
            base_image = self.draw_round_corner_rectangle(
                base_image,
                (left, top, right, bottom),
                self.config.attack_rect_radius,
                self.config.attack_rect_fill,
                self.config.attack_rect_outline_color,
                self.config.attack_rect_outline_width,
            )
            left_pointer = left + self.config.attack_padding
            attack_top = int(
                self.config.attack_rect_top
                + (self.config.attack_rect_height - self.config.attack_icon_width) / 2
            )
            base_image.paste(
                attack_image,
                (left_pointer, attack_top),
                mask=attack_image,
            )
            left_pointer += self.config.attack_icon_width + self.config.attack_padding
            attack_text_top = int(
                self.config.attack_rect_top
                + (
                    self.config.attack_rect_height
                    - font.getsize(str(card_info.attack))[1]
                )
                / 2
                - self.config.attack_font_compensation
            )
            base_image = self.add_text_on_image(
                base_image,
                str(card_info.attack),
                (left_pointer, attack_text_top),
                font,
                self.config.attack_font_color,
            )
        return base_image

    def get_power_image(self):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "power")
        )

    def get_duration_image(self):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "duration")
        )

    def draw_power_or_duration(self, card_info: CardInfo, base_image: PIL.Image):
        image = None
        text = ""
        if card_info.duration < 0 and card_info.power < 0:
            return base_image
        if card_info.duration >= 0:
            image = self.get_duration_image()
            text = str(card_info.duration)
        else:
            image = self.get_power_image()
            text = str(card_info.power)
        image = self.adjust_image(
            image,
            (
                self.config.power_or_duration_icon_width,
                self.config.power_or_duration_icon_width,
            ),
        )
        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.power_or_duration_font),
            self.config.power_or_duration_font_size,
        )
        estimated_length = (
            font.getsize(text)[0]
            + self.config.power_or_duration_padding * 3
            + self.config.power_or_duration_icon_width
        )
        right = self.config.power_or_duration_rect_right
        top = self.config.power_or_duration_rect_top
        left = right - estimated_length
        bottom = top + self.config.power_or_duration_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (left, top, right, bottom),
            self.config.power_or_duration_rect_radius,
            self.config.power_or_duration_rect_fill,
            self.config.power_or_duration_rect_outline_color,
            self.config.power_or_duration_rect_outline_width,
        )

        right_pointer = (
            right - self.config.power_or_duration_padding - font.getsize(text)[0]
        )
        power_or_duration_text_top = int(
            self.config.power_or_duration_rect_top
            + (self.config.power_or_duration_rect_height - font.getsize(text)[1]) / 2
            - self.config.power_or_duration_font_compensation
        )
        base_image = self.add_text_on_image(
            base_image,
            text,
            (right_pointer, power_or_duration_text_top),
            font,
            self.config.power_or_duration_font_color,
        )
        right_pointer -= self.config.life_icon_width + self.config.life_padding
        power_or_duration_top = int(
            self.config.power_or_duration_rect_top
            + (
                self.config.power_or_duration_rect_height
                - self.config.power_or_duration_icon_width
            )
            / 2
        )

        base_image.paste(
            image,
            (right_pointer, power_or_duration_top),
            mask=image,
        )

        return base_image

    def draw_expense(self, card_info: CardInfo, base_image: PIL.Image):
        # estimate the length
        all_expenses = []
        for ele in card_info.elements_expense.keys():
            if card_info.elements_expense[ele] > 0:
                all_expenses.append((ele, card_info.elements_expense[ele]))
        # nothing to do here
        if len(all_expenses) == 0:
            return base_image

        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.expense_font),
            self.config.expense_font_size,
        )

        number_length = 0
        for tup in all_expenses:
            number_length += font.getsize(str(tup[1]))[0]
        category_length = len(all_expenses) * self.config.expense_category_width
        total_length = (
            number_length
            + category_length
            + len(all_expenses) * self.config.expense_padding * 2
            + self.config.expense_padding
        )
        # draw the rectangle
        rect_top = self.config.expense_rect_top
        rect_right = self.config.expense_rect_right
        rect_left = rect_right - total_length
        rect_bottom = rect_top + self.config.expense_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (rect_left, rect_top, rect_right, rect_bottom),
            self.config.expense_rect_radius,
            self.config.expense_rect_fill,
            self.config.expense_rect_outline_color,
            self.config.expense_rect_outline_width,
        )
        # put in the numbers and categories
        text_height = font.getsize("8")[1]
        right_pointer = (
            rect_right
            - self.config.expense_padding
            - self.config.expense_category_width
        )

        text_top = int(
            rect_top
            + (self.config.expense_rect_height - text_height) / 2
            - self.config.expense_font_compensation
        )
        category_top = int(
            rect_top
            + (self.config.expense_rect_height - self.config.expense_category_width) / 2
        )
        # sort all expenses, put the corresponding element to the head
        for tup in all_expenses:
            if tup[0] == card_info.category:
                all_expenses.remove(tup)
                all_expenses.insert(0, tup)
                break
        all_expenses = reversed(all_expenses)
        # draw the elements
        for tup in all_expenses:
            # draw the category
            category_image = self.get_category_image(tup[0])
            category_image = self.adjust_image(
                category_image,
                (
                    self.config.expense_category_width,
                    self.config.expense_category_width,
                ),
            )
            base_image.paste(
                category_image,
                (right_pointer, category_top),
                mask=category_image,
            )
            right_pointer -= font.getsize(str(tup[1]))[0] + self.config.expense_padding

            # draw the number
            base_image = self.add_text_on_image(
                base_image,
                str(tup[1]),
                (right_pointer, text_top),
                font,
                self.config.expense_font_color,
            )
            right_pointer -= (
                self.config.expense_category_width + self.config.expense_padding
            )

        return base_image

    def draw_number(self, card_info: CardInfo, base_image: PIL.Image):
        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.number_font),
            self.config.number_font_size,
        )
        color = self.config.number_font_color
        if self.config.reverse_color_for_hero and card_info.type == "英雄":
            color = self.reverse_color(color)
        base_image = self.add_text_on_image(
            base_image,
            "No." + str(card_info.number),
            (
                self.config.card_width
                - self.config.number_text_to_right
                - font.getsize("No." + str(card_info.number))[0],
                self.config.drawing_to_upper
                + self.config.drawing_height
                + self.config.number_text_to_block_top,
            ),
            font,
            color,
        )
        return base_image

    def make_unit_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        # 准备费用
        base_image = self.draw_cost(card_info, base_image)
        # 准备标签
        base_image = self.draw_tag(card_info, base_image)
        # 准备卡牌描述和引言
        base_image = self.draw_discription_and_quote(card_info, base_image)
        # 准备底部负载
        base_image = self.draw_gain(card_info, base_image)
        # 绘制生命和攻击
        base_image = self.draw_life_and_attack(card_info, base_image)
        # 准备卡牌编号
        base_image = self.draw_number(card_info, base_image)

        return base_image

    def make_ability_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        # 准备费用
        base_image = self.draw_cost(card_info, base_image)
        # 准备代价
        base_image = self.draw_expense(card_info, base_image)
        # 准备标签
        base_image = self.draw_tag(card_info, base_image)
        # 准备卡牌描述和引言
        base_image = self.draw_discription_and_quote(card_info, base_image)
        # 准备威力或持续时间
        base_image = self.draw_power_or_duration(card_info, base_image)
        # 准备卡牌编号
        base_image = self.draw_number(card_info, base_image)
        # 准备生命和攻击
        base_image = self.draw_life_and_attack(card_info, base_image)
        return base_image

    def make_item_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        # 准备费用
        base_image = self.draw_cost(card_info, base_image)
        # 准备代价
        base_image = self.draw_expense(card_info, base_image)
        # 准备标签
        base_image = self.draw_tag(card_info, base_image)
        # 准备卡牌描述和引言
        base_image = self.draw_discription_and_quote(card_info, base_image)
        # 准备底部负载
        base_image = self.draw_gain(card_info, base_image)
        # 准备威力或者持续
        base_image = self.draw_power_or_duration(card_info, base_image)
        # 准备卡牌编号
        base_image = self.draw_number(card_info, base_image)
        # 绘制生命和攻击
        base_image = self.draw_life_and_attack(card_info, base_image)
        return base_image

    def make_hero_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        # 准备费用
        base_image = self.draw_cost(card_info, base_image)
        # 准备标签
        base_image = self.draw_tag(card_info, base_image)
        # 准备卡牌描述和引言
        base_image = self.draw_discription_and_quote(card_info, base_image)
        # 准备底部负载
        base_image = self.draw_gain(card_info, base_image)
        # 准备生命和攻击
        base_image = self.draw_life_and_attack(card_info, base_image)
        # 准备卡牌编号
        base_image = self.draw_number(card_info, base_image)
        return base_image

    def make_card(self, card_info: CardInfo):
        if card_info.type == "生物":
            result = self.make_unit_card(card_info)
            return result
        elif card_info.type == "技能":
            result = self.make_ability_card(card_info)
            return result
        elif card_info.type == "道具":
            result = self.make_item_card(card_info)
            return result
        elif card_info.type == "英雄":
            result = self.make_hero_card(card_info)
            return result
