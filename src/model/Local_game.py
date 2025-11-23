import pygame
import random
from model.single_game import SingleGame
from model.config import Config


class LocalGame(SingleGame):
    def __init__(self):
        super().__init__()
        # 初始化AI蛇
        self.ai_snake = [(20, 10), (19, 10), (18, 10)]
        self.ai_velocity = (1, 0)
        self.ai_last_velocity = (1, 0)

        # 从Config读取边界（左,右）、（上,下）
        self.border_left, self.border_right = Config().border_x
        self.border_top, self.border_bottom = Config().border_y

    def reset(self):
        super().reset()
        # 重置AI蛇状态
        self.ai_snake = [(20, 10), (19, 10), (18, 10)]
        self.ai_velocity = (1, 0)
        self.ai_last_velocity = (1, 0)

    def ai_move(self):
        """优化后AI蛇移动逻辑：优先避障，再追食物"""
        if self.game_over:
            return

        head_x, head_y = self.ai_snake[0]
        available_dirs = []  # 存储安全方向：(dx, dy)

        # 1. 筛选所有安全方向（不撞墙、不撞自身）
        possible_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 所有可能方向
        for dx, dy in possible_dirs:
            # 计算该方向的新头部
            test_head = (head_x + dx, head_y + dy)
            # 检查是否撞墙（边界检测）
            if not (
                self.border_left <= test_head[0] <= self.border_right
                and self.border_top <= test_head[1] <= self.border_bottom
            ):
                continue
            # 检查是否撞自身（排除蛇头，只看身体）
            if test_head in self.ai_snake[1:]:
                continue
            # 检查是否反向（避免回头撞自己）
            if (dx, dy) == (-self.ai_last_velocity[0], -self.ai_last_velocity[1]):
                continue
            # 所有检查通过，加入安全方向列表
            available_dirs.append((dx, dy))

        # 2. 从安全方向中选择最优方向（最接近食物）
        if available_dirs:
            if self.foods:
                target = self._find_nearest_food()
                # 计算每个安全方向到食物的曼哈顿距离，选距离最小的
                available_dirs.sort(
                    key=lambda dir: abs((head_x + dir[0]) - target[0])
                    + abs((head_y + dir[1]) - target[1])
                )
            # 选择最优方向（距离最近/默认第一个安全方向）
            self.ai_velocity = available_dirs[0]
        else:
            # 极端情况：无安全方向（死路），维持原方向（游戏结束）
            self.ai_velocity = self.ai_last_velocity

        # 3. 计算新头部并执行移动
        new_head = (head_x + self.ai_velocity[0], head_y + self.ai_velocity[1])
        self.ai_last_velocity = self.ai_velocity  # 记录上一次方向，避免反向

        # 最终碰撞检测（与玩家蛇、极端边界）
        if (
            self.collision_detector.check_collision(new_head, self.ai_snake)
            or new_head in self.snake
        ):
            self.game_over = True
            return

        # 最终碰撞检测：添加与玩家蛇的碰撞检测
        if self.collision_detector.check_collision(
            new_head, self.ai_snake
        ) or self.collision_detector.check_other_snake_collision(new_head, self.snake):
            self.game_over = True
            return

        # 更新AI蛇身
        self.ai_snake.insert(0, new_head)
        if new_head in self.foods:
            self.food_manager.remove_food(new_head)
            self.generate_food(1)
        else:
            self.ai_snake.pop()


    def move_snake(self):
        """重写玩家蛇移动方法，添加与 AI 蛇的碰撞检测"""
        if not self.is_running or self.velocity == (0, 0) or self.game_over:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.velocity[0], head_y + self.velocity[1])

        # 碰撞检测：边界、自身、AI 蛇
        collision = self.collision_detector.check_collision(new_head, self.snake)
        # 新增：检测玩家蛇是否碰撞 AI 蛇
        if new_head in self.ai_snake:
            collision = True

        if collision:
            self.game_over = True
            return
        
        # 以下保持原有更新蛇身的逻辑
        self.snake.insert(0, new_head)
        if self.food_manager.check_food_collision(new_head):
            self.food_manager.remove_food(new_head)
            self.generate_food(1)
        else:
            self.snake.pop()

    def _find_nearest_food(self):
        """找到离AI蛇头最近的食物"""
        head = self.ai_snake[0]
        return min(self.foods, key=lambda f: abs(f[0] - head[0]) + abs(f[1] - head[1]))
