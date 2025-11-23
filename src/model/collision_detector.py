class CollisionDetector:
    """碰撞检测工具类"""

    def __init__(self, config):
        self.config = config

    def check_border_collision(self, position):
        """检查边界碰撞"""
        x, y = position
        return (
            x < self.config.border_x[0]
            or x > self.config.border_x[1]
            or y < self.config.border_y[0]
            or y > self.config.border_y[1]
        )

    def check_self_collision(self, position, snake_body):
        """检查自身碰撞"""
        return position in snake_body

    def check_collision(self, position, snake_body):
        """检查任何类型的碰撞"""
        return self.check_border_collision(position) or self.check_self_collision(
            position, snake_body
        )

    def check_other_snake_collision(self, position, other_snake):
        """检查与其他蛇的碰撞"""
        return position in other_snake
