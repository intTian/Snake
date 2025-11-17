import random
from utils.config import *


class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.random_spawn([])  # 初始生成（无蛇时直接随机）

    # 随机生成食物（传入所有蛇的身体，避免重叠）
    def random_spawn(self, all_snake_bodies):
        # 计算可生成的网格坐标（确保食物对齐网格）
        max_x = (SCREEN_WIDTH // GRID_SIZE) - 1
        max_y = (SCREEN_HEIGHT // GRID_SIZE) - 1
        while True:
            # 随机生成网格索引，再转换为像素坐标
            grid_x = random.randint(0, max_x)
            grid_y = random.randint(0, max_y)
            self.x = grid_x * GRID_SIZE
            self.y = grid_y * GRID_SIZE
            # 检查是否与蛇身重叠，不重叠则退出循环
            if (self.x, self.y) not in all_snake_bodies:
                break
