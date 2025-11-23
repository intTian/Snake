import pygame
from pygame.locals import *  # type: ignore
from lib.ui.animation import SnakeAnimation
from lib.ui.background import StartBackground
from lib.ui.button import Button
from lib.ui.title import Title


class StartView:
    """开始游戏视图：负责所有UI绘制，不处理业务逻辑"""

    def __init__(self, width, height, font_manager, color_palette, title):
        # 接收控制器传递的工具类和配置
        self.font_manager = font_manager
        self.color_palette = color_palette

        # 创建窗口（视图持有显示表面，控制器不直接操作）
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self._set_icon()

        # 创建所有UI组件（子视图）
        self.background = StartBackground(color_palette)
        self.title = Title("贪吃蛇大作战", "经典游戏体验", font_manager, color_palette)
        self.snake_anim = SnakeAnimation(color_palette)
        self.buttons = self._create_buttons(width, height)

    def _set_icon(self):
        """设置窗口图标（视图负责UI相关配置）"""
        try:
            icon = pygame.image.load("resource\\snake_icon.ico").convert_alpha()
            pygame.display.set_icon(icon)
        except:
            print("警告：未找到图标文件，使用默认图标")

    def _create_buttons(self, init_width, init_height):
        """创建按钮（视图负责UI组件初始化）"""
        buttons = [
            Button(
                0.5 - 0.375 / 2,  # 相对X（居中）
                0.4,  # 相对Y（上移位置，保持间距一致）
                0.375,  # 相对宽度
                0.1,  # 相对高度
                "单人模式",
                "single",
                self.font_manager,
                self.color_palette,
            ),
            Button(
                0.5 - 0.375 / 2,
                0.55,  # 与上一个按钮保持0.15的垂直间距
                0.375,
                0.1,
                "人机对战",
                "local",
                self.font_manager,
                self.color_palette,
            ),
            Button(
                0.5 - 0.375 / 2,
                0.7,  # 保持与上一个按钮0.15的垂直间距
                0.375,
                0.1,
                "退出游戏",
                "quit",
                self.font_manager,
                self.color_palette,
            ),
        ]

        # 初始化时计算绝对坐标
        for btn in buttons:
            btn.update_rect(init_width, init_height)
        return buttons

    def update_button_hover(self, mouse_pos):
        """更新按钮悬停状态（只接收控制器传递的鼠标位置，不处理逻辑）"""
        for btn in self.buttons:
            btn.check_hover(mouse_pos)

    def check_button_click(self, mouse_pos):
        """检查按钮点击（返回点击的动作，由控制器处理逻辑）"""
        for btn in self.buttons:
            if btn.is_clicked(mouse_pos):
                return btn.get_action()  # 只返回结果，不处理动作
        return None

    def update_animations(self, width, height):
        """更新动态UI（标题、蛇动画、背景）"""
        self.title.update()
        self.snake_anim.update(width, height)
        self.background.update()

    def resize(self, new_width, new_height):
        """窗口缩放时同步更新UI尺寸（视图负责适配）"""
        for btn in self.buttons:
            btn.update_rect(new_width, new_height)

    def draw(self, width, height):
        """绘制所有UI元素（视图核心方法）"""
        # 绘制背景
        self.background.draw(self.screen, width, height)
        # 绘制标题
        self.title.draw(self.screen, width, height)
        # 绘制蛇动画
        self.snake_anim.draw(self.screen, width, height)
        # 绘制按钮
        for btn in self.buttons:
            btn.draw(self.screen)
        # 更新显示
        pygame.display.flip()
