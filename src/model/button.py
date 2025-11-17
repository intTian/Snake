import pygame
import sys


# 按钮类
class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        font_size: int = 30,
        bg_color: tuple = (70, 70, 70),  # 正常背景色
        hover_color: tuple = (100, 100, 100),  # 悬停背景色
        click_color: tuple = (50, 50, 50),  # 点击背景色
        text_color: tuple = (255, 255, 255),  # 文本颜色
        border_radius: int = 5,
    ):  # 圆角半径

        # 按钮位置和大小
        self.rect = pygame.Rect(x, y, width, height)

        # 颜色配置
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color

        # 状态标识
        self.is_hovered = False
        self.is_clicked = False

        # 文本配置
        self.text = text
        self.font = pygame.font.SysFont("Microsoft YaHei UI", font_size)
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # 外观配置
        self.border_radius = border_radius

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件，返回是否被点击"""
        if event.type == pygame.MOUSEMOTION:
            # 检测鼠标悬停
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.is_clicked = False  # 鼠标移动时重置点击状态

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检测鼠标按下
            if event.button == 1 and self.is_hovered:  # 左键点击
                self.is_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # 检测鼠标释放（完整点击动作）
            if event.button == 1 and self.is_clicked:
                self.is_clicked = False
                return True  # 返回点击成功

        return False

    def draw(self, surface: pygame.Surface) -> None:
        """绘制按钮到指定表面"""
        # 根据状态选择背景色
        if self.is_clicked:
            current_color = self.click_color
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.bg_color

        # 绘制按钮背景（支持圆角）
        pygame.draw.rect(
            surface, current_color, self.rect, border_radius=self.border_radius
        )

        # 绘制按钮文本（居中）
        surface.blit(self.text_surface, self.text_rect)

    def set_text(self, text: str) -> None:
        """更新按钮文本"""
        self.text = text
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def move(self, x: int, y: int) -> None:
        """移动按钮位置"""
        self.rect.topleft = (x, y)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
