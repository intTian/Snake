import pygame
from controller.game_ui import GameUI
from model.snake import Snake
from model.food import Food
from model.collision import check_snake_food_collision
from utils.config import *


class SinglePlayerMode:
    def __init__(self):
        self.ui = GameUI()
        self.snake = Snake(is_ai=False)
        self.food = Food()
        self.is_paused = False
        self.is_game_over = False

    # 按键处理
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # 暂停/继续
                if event.key == KEY_PAUSE:
                    self.is_paused = not self.is_paused
                # 重新开始
                if event.key == KEY_RESTART:
                    self.reset_game()
                # 帮助（可弹窗显示按键说明，简化版直接打印）
                if event.key == KEY_HELP:
                    print("按键说明：方向键/WASD 移动，P 暂停，R 重启，H 帮助")
                # 移动方向控制（仅游戏未暂停、未结束时生效）
                if not self.is_paused and not self.is_game_over:
                    if event.key in KEY_UP:
                        self.snake.change_direction(0, -GRID_SIZE)
                    elif event.key in KEY_DOWN:
                        self.snake.change_direction(0, GRID_SIZE)
                    elif event.key in KEY_LEFT:
                        self.snake.change_direction(-GRID_SIZE, 0)
                    elif event.key in KEY_RIGHT:
                        self.snake.change_direction(GRID_SIZE, 0)

    # 重置游戏
    def reset_game(self):
        self.snake = Snake(is_ai=False)
        self.food = Food()
        self.is_paused = False
        self.is_game_over = False

    # 游戏主循环
    def run(self):
        while True:
            self.handle_events()
            if not self.is_paused and not self.is_game_over:
                # 蛇移动
                self.snake.move()
                # 检测吃食物
                if check_snake_food_collision(self.snake, self.food):
                    self.snake.grow()
                    # 重新生成食物（传入蛇身避免重叠）
                    self.food.random_spawn(self.snake.body)
                # 检测失败
                if (
                    self.snake.check_self_collision()
                    or self.snake.check_bound_collision()
                ):
                    self.is_game_over = True

            # 绘制界面
            self.ui.clear()
            self.ui.draw_snake([self.snake])
            self.ui.draw_food(self.food)
            self.ui.draw_text(f"分数：{self.snake.score}", 20, 20)
            # 显示状态提示
            if self.is_paused:
                self.ui.draw_text(
                    "暂停中（按 P 继续）", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2
                )
            if self.is_game_over:
                self.ui.draw_text(
                    "游戏结束（按 R 重启）", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2
                )
            # 刷新界面
            self.ui.update()
