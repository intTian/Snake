import math

from utils.color import ColorPalette
from utils.font import FontManager  # 导入数学库，用于动画计算


class Title:
    """标题组件，负责绘制游戏标题和副标题，包含简单动画效果"""

    def __init__(self, main_text, sub_text, font_manager=None, color_palette=None):
        """初始化标题
        :param main_text: 主标题文本（字符串）
        :param sub_text: 副标题文本（字符串）
        :param font_manager: 字体管理器实例，默认为None时使用默认字体配置
        :param color_palette: 颜色管理器实例，默认为None时使用默认颜色配置
        """
        self.main_text = main_text  # 主标题文本内容
        self.sub_text = sub_text  # 副标题文本内容
        # 初始化字体管理器，若未传入则使用默认实例
        self.font_manager = font_manager or FontManager()
        # 初始化颜色管理器，若未传入则使用默认实例
        self.color_palette = color_palette or ColorPalette()
        self.oscillation = 0  # 振荡动画参数（用于标题上下浮动）

    def update(self):
        """更新标题动画（振荡效果）"""
        # 增加振荡参数，用于后续sin函数计算（控制浮动速度）
        self.oscillation += 0.05

    def draw(self, surface, win_width, win_height):
        """绘制标题
        :param surface: 绘制表面（pygame的Surface对象）
        :param win_width: 窗口宽度
        :param win_height: 窗口高度
        """
        # 计算标题Y坐标：基础位置为窗口高度的15%，叠加sin振荡（范围±5像素）
        title_y = win_height * 0.15 + math.sin(self.oscillation) * 5

        # 绘制主标题
        # 1. 创建主标题文本表面（使用大字体和标题色）
        title_text = self.font_manager.get_large_font().render(
            self.main_text, True, self.color_palette.get_title_color()
        )
        # 2. 创建主标题阴影（灰色，用于增强立体感）
        title_shadow = self.font_manager.get_large_font().render(
            self.main_text, True, (100, 100, 100)
        )
        # 3. 计算主标题X坐标（水平居中）
        title_x = win_width // 2 - title_text.get_width() // 2
        # 4. 先绘制阴影（偏移2像素），再绘制主标题
        surface.blit(title_shadow, (title_x + 2, title_y + 2))
        surface.blit(title_text, (title_x, title_y))

        # 绘制副标题
        # 1. 创建副标题文本表面（使用小字体和描述文本色）
        subtitle = self.font_manager.get_small_font().render(
            self.sub_text, True, self.color_palette.get_description_color()
        )
        # 2. 计算副标题X坐标（水平居中）
        subtitle_x = win_width // 2 - subtitle.get_width() // 2
        # 3. 绘制副标题（位于主标题下方80像素）
        surface.blit(subtitle, (subtitle_x, title_y + 80))
