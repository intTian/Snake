import pygame
import random
from model.config import Config
from model.collision_detector import CollisionDetector
from model.food_manager import FoodManager


class SingleGame:
    def __init__(self):
        # 初始化游戏状态（新增重置方法所需的基础配置）
        self.initial_snake = [(10, 10), (9, 10), (8, 10)]
        self.reset()  # 初始化时调用重置方法

        # 组件初始化
        self.config = Config()
        self.collision_detector = CollisionDetector(self.config)
        self.food_manager = FoodManager(self.config)

    def reset(self):
        """重置游戏状态（新增方法）"""
        self.snake = self.initial_snake.copy()
        self.velocity = (0, 0)
        self.last_velocity = (1, 0)
        self.is_running = True
        self.game_over = False  # 新增游戏结束标志

    def generate_food(self, count=1):
        """生成指定数量的食物（避免与蛇身重叠）"""
        self.food_manager.generate_food(count, self.snake)

    def move_snake(self):
        """根据速度向量移动蛇（速度为(0,0)时不移动）"""
        # 若游戏未运行、速度为零或已结束，则不执行移动逻辑
        if not self.is_running or self.velocity == (0, 0) or self.game_over:
            return

        # 计算新头部坐标：基于当前头部位置和速度向量
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.velocity[0], head_y + self.velocity[1])

        # 碰撞检测：检查新头部是否碰撞边界或自身
        if self.collision_detector.check_collision(new_head, self.snake):
            self.game_over = True  # 标记游戏结束（但不直接退出）
            return
        
        # 更新蛇身：在头部插入新位置（实现移动效果）
        self.snake.insert(0, new_head)

        # 吃食物逻辑：
        # 若新头部位置有食物，则移除该食物并生成新食物（蛇身增长）
        # 若没有吃到食物，则移除尾部（保持长度不变）
        if self.food_manager.check_food_collision(new_head):
            self.food_manager.remove_food(new_head)
            self.generate_food(1)
        else:
            self.snake.pop()

    def set_velocity(self, key, is_pressed):
        """简化逻辑：记录上一速度，静止后禁止按上一速度的反向键启动"""
        # 按键-速度映射
        key_map = {
            # 方向键
            pygame.K_UP: (0, -1),  # 上
            pygame.K_DOWN: (0, 1),  # 下
            pygame.K_LEFT: (-1, 0),  # 左
            pygame.K_RIGHT: (1, 0),  # 右
            # WASD键
            pygame.K_w: (0, -1),  # W键对应上
            pygame.K_s: (0, 1),  # S键对应下
            pygame.K_a: (-1, 0),  # A键对应左
            pygame.K_d: (1, 0),  # D键对应右
        }
        target_vel = key_map.get(key)
        if not target_vel:
            return

        # 按键按下时
        if is_pressed:
            # 静止状态：禁止按上一次速度的反向键
            if self.velocity == (0, 0):
                reverse_last = (-self.last_velocity[0], -self.last_velocity[1])
                if target_vel == reverse_last:
                    return  # 反向键直接丢弃
                # 非反向：更新速度并记录为当前速度
                self.velocity = target_vel
            # 移动状态：正常更新速度（覆盖上一速度）
            else:
                if target_vel == (-self.velocity[0], -self.velocity[1]):
                    return
                self.velocity = target_vel
        # 按键松开时
        else:
            # 松开当前速度对应的按键 → 静止，并记录当前速度为上一速度
            if self.velocity == target_vel:
                self.last_velocity = self.velocity  # 保存上一次移动方向
                self.velocity = (0, 0)  # 静止

    @property
    def foods(self):
        """保持原有接口，提供食物列表访问"""
        return self.food_manager.foods
