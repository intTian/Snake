def check_snake_food_collision(snake, food):
    """检测蛇是否吃到食物"""
    return snake.body[0] == (food.x, food.y)

def check_snake_snake_collision(snake1, snake2):
    """检测两条蛇是否碰撞（蛇头撞对方蛇身）"""
    return snake1.body[0] in snake2.body or snake2.body[0] in snake1.body