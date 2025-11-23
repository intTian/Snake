class ColorPalette:
    """颜色管理类，集中管理所有UI颜色，便于统一修改和维护"""

    def __init__(self):
        """初始化颜色配置（RGB格式，每个值范围0-255）"""
        self.BACKGROUND_COLOR = (10, 10, 30)  # 背景基础色（深紫黑）
        self.GRADIENT_COLORS = [
            (30, 30, 80),
            (50, 20, 100),
            (20, 50, 120),
        ]  # 渐变三色（深蓝到紫色系）
        self.BUTTON_COLOR = (60, 130, 240)  # 按钮默认色（亮蓝）
        self.BUTTON_HOVER_COLOR = (100, 160, 255)  # 按钮悬停色（浅蓝）
        self.BUTTON_TEXT_COLOR = (255, 255, 255)  # 按钮文本色（白色）
        self.TITLE_COLOR = (255, 215, 0)  # 标题色（金色）
        self.DESCRIPTION_COLOR = (200, 200, 255)  # 描述文本色（浅紫白）

    def get_background_color(self):
        """获取背景色"""
        return self.BACKGROUND_COLOR

    def get_gradient_colors(self):
        """获取渐变颜色列表（用于背景渐变）"""
        return self.GRADIENT_COLORS

    def get_button_color(self, hover=False):
        """获取按钮颜色
        :param hover: 是否为悬停状态，True返回悬停色，False返回默认色
        """
        return self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR

    def get_button_text_color(self):
        """获取按钮文本颜色"""
        return self.BUTTON_TEXT_COLOR

    def get_title_color(self):
        """获取标题颜色"""
        return self.TITLE_COLOR

    def get_description_color(self):
        """获取描述文本颜色"""
        return self.DESCRIPTION_COLOR
