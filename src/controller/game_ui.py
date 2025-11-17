import pygame
from utils.config import *


class GameUI:
    def __init__(self):
        pygame.init()  # 初始化 Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()  # 控制帧率
        self.font = pygame.font.SysFont("Microsoft YaHei UI", 24)  # 文字字体

    # 绘制蛇（接收蛇对象列表，支持多条蛇）
    def draw_snake(self, snakes):
        for snake in snakes:
            for segment in snake.body:  # snake.body 是坐标列表 [(x1,y1), (x2,y2)...]
                pygame.draw.rect(
                    self.screen,
                    snake.color,
                    (segment[0], segment[1], GRID_SIZE, GRID_SIZE),
                )

    # 绘制食物
    def draw_food(self, food):
        pygame.draw.rect(
            self.screen, FOOD_COLOR, (food.x, food.y, GRID_SIZE, GRID_SIZE)
        )

    # 显示文字（如分数、提示）
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    # 刷新界面
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)  # 固定帧率

    # 清空屏幕（每帧绘制前调用）
    def clear(self):
        self.screen.fill(BACKGROUND_COLOR)
