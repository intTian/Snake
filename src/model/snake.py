from utils.config import *


class Snake:
    def __init__(self, is_ai=False):
        self.is_ai = is_ai  # 是否为 AI 蛇
        self.color = AI_SNAKE_COLOR if is_ai else SNAKE_COLOR
        # 初始位置（窗口中心）
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        # 初始方向（向右）：dx=水平偏移，dy=垂直偏移（每帧移动 GRID_SIZE 像素）
        self.dx = GRID_SIZE
        self.dy = 0
        # 蛇身：列表存储每个 segments 的 (x,y) 坐标，头部在列表第一个元素
        self.body = [(self.x - i * GRID_SIZE, self.y) for i in range(SNAKE_INIT_LEN)]
        self.score = 0  # 分数

    # 移动逻辑：头部向前，尾部删除（增长时不删除尾部）
    def move(self, grow=False):
        # 计算新头部坐标
        new_head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
        # 头部插入到蛇身最前
        self.body.insert(0, new_head)
        # 不增长则删除尾部
        if not grow:
            self.body.pop()

    # 改变方向（禁止反向）
    def change_direction(self, new_dx, new_dy):
        # 例如：当前向右（dx=GRID_SIZE），不能直接向左（dx=-GRID_SIZE）
        if (new_dx != -self.dx) or (new_dy != -self.dy):
            self.dx = new_dx
            self.dy = new_dy

    # 增长（吃食物后调用）
    def grow(self):
        self.score += FOOD_SCORE
        self.move(grow=True)  # 移动时不删除尾部，实现增长

    # 碰撞自身检测
    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    # 碰撞边界检测
    def check_bound_collision(self):
        head_x, head_y = self.body[0]
        return (
            (head_x < 0)
            or (head_x >= SCREEN_WIDTH)
            or (head_y < 0)
            or (head_y >= SCREEN_HEIGHT)
        )
