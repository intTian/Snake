# src/view/ai_view.py
import pygame
from view.single_view import SingleView


class LocalView(SingleView):
    def draw_snake(self):
        # 绘制玩家蛇
        super().draw_snake()
        # 绘制AI蛇（红色）
        if not self.model.ai_snake:
            return

        # AI蛇身
        for i, (x, y) in enumerate(self.model.ai_snake):
            color = (255, 100, 100) if i > 0 else (255, 0, 0)  # 红色AI蛇
            pygame.draw.rect(
                self.screen,
                color,
                (
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1,
                ),
                border_radius=3,
            )
