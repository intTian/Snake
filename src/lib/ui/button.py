import math  # 导入数学库，用于动画计算
import pygame

from utils.color import ColorPalette
from utils.font import FontManager  # 导入pygame库，用于图形绘制


class Button:
    """按钮组件类，支持缩放和悬停效果，响应鼠标交互"""

    def __init__(
        self,
        x_ratio,
        y_ratio,
        width_ratio,
        height_ratio,
        text,
        action=None,
        font_manager=None,
        color_palette=None,
    ):
        """初始化按钮
        :param x_ratio: x坐标相对窗口宽度的比例（0-1，如0.5表示居中）
        :param y_ratio: y坐标相对窗口高度的比例（0-1）
        :param width_ratio: 宽度相对窗口宽度的比例（0-1）
        :param height_ratio: 高度相对窗口高度的比例（0-1）
        :param text: 按钮文本（字符串）
        :param action: 按钮点击事件（回调函数），默认为None
        :param font_manager: 字体管理器实例，默认为None时使用默认配置
        :param color_palette: 颜色管理器实例，默认为None时使用默认配置
        """
        self.x_ratio = x_ratio  # x坐标比例
        self.y_ratio = y_ratio  # y坐标比例
        self.width_ratio = width_ratio  # 宽度比例
        self.height_ratio = height_ratio  # 高度比例
        self.text = text  # 按钮文本
        self.action = action  # 点击事件回调
        self.hover = False  # 是否悬停状态（默认否）
        self.radius = 15  # 按钮圆角半径
        self.pulse = 0  # 脉冲动画参数（用于悬停缩放）
        self.rect = pygame.Rect(0, 0, 0, 0)  # 按钮矩形区域（初始化为空）

        # 初始化字体管理器，若未传入则使用默认实例
        self.font_manager = font_manager or FontManager()
        # 初始化颜色管理器，若未传入则使用默认实例
        self.color_palette = color_palette or ColorPalette()

    def update_rect(self, win_width, win_height):
        """根据窗口大小更新按钮位置和尺寸（适配窗口缩放）
        :param win_width: 窗口宽度
        :param win_height: 窗口高度
        """
        self.rect.x = win_width * self.x_ratio  # 计算实际x坐标
        self.rect.y = win_height * self.y_ratio  # 计算实际y坐标
        self.rect.width = win_width * self.width_ratio  # 计算实际宽度
        self.rect.height = win_height * self.height_ratio  # 计算实际高度

    def draw(self, surface):
        """绘制按钮
        :param surface: 绘制表面（pygame的Surface对象）
        """
        if self.hover:
            # 悬停时：更新脉冲动画参数（0到π循环）
            self.pulse = (self.pulse + 0.05) % math.pi
            # 计算脉冲偏移量（sin函数控制，范围±5像素）
            pulse_offset = int(5 * math.sin(self.pulse))
            # 计算脉冲后的矩形（原矩形扩大偏移量）
            pulse_rect = self.rect.inflate(pulse_offset, pulse_offset)
            # 获取悬停状态的按钮颜色
            color = self.color_palette.get_button_color(True)
            # 计算发光颜色（比按钮色亮30，不超过255）
            glow_color = (
                min(255, color[0] + 30),
                min(255, color[1] + 30),
                min(255, color[2] + 30),
            )
            # 绘制发光效果（带圆角）
            pygame.draw.rect(
                surface, glow_color, pulse_rect, border_radius=self.radius + 2
            )

        # 绘制按钮主体（根据悬停状态选择颜色）
        current_color = self.color_palette.get_button_color(self.hover)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.radius)

        # 绘制按钮文本
        # 1. 创建文本表面（中字体，白色文本）
        text_surf = self.font_manager.get_medium_font().render(
            self.text, True, self.color_palette.get_button_text_color()
        )
        # 2. 计算文本位置（居中于按钮）
        text_rect = text_surf.get_rect(center=self.rect.center)
        # 3. 绘制文本
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        """检查鼠标是否悬停在按钮上
        :param pos: 鼠标位置（(x,y)元组）
        """
        # 若鼠标位置在按钮矩形内，则设为悬停状态
        self.hover = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        """检查按钮是否被点击
        :param pos: 点击位置（(x,y)元组）
        :return: 是否点击了按钮（布尔值）
        """
        return self.rect.collidepoint(pos)

    def get_action(self):
        """获取按钮点击事件（回调函数）"""
        return self.action

