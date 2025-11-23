import random


class FoodManager:
    """食物生成和管理类"""

    def __init__(self, config):
        self.config = config
        self.foods = []  # 存储多个食物坐标

    def generate_food(self, count=1, snake_body=None):
        """生成指定数量的食物（避免与蛇身重叠）"""
        snake_body = snake_body or []
        for _ in range(count):
            while True:
                x = random.randint(self.config.border_x[0], self.config.border_x[1])
                y = random.randint(self.config.border_y[0], self.config.border_y[1])
                if (x, y) not in snake_body and (x, y) not in self.foods:
                    self.foods.append((x, y))
                    break

    def check_food_collision(self, position):
        """检查是否吃到食物"""
        return position in self.foods

    def remove_food(self, position):
        """移除被吃掉的食物"""
        if position in self.foods:
            self.foods.remove(position)
