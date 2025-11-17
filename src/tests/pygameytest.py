import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# 设置窗口标题
pygame.display.set_caption("Animation with Frame Rate Control")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 初始化矩形位置和速度
rect = pygame.Rect(100, 100, 50, 50)
rect_speed = [2, 2]

# 创建时钟对象
clock = pygame.time.Clock()

# 主循环标志
running = True

# 主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 移动矩形
    rect.x += rect_speed[0]
    rect.y += rect_speed[1]

    # 碰到边界反弹
    if rect.left < 0 or rect.right > window_size[0]:
        rect_speed[0] = -rect_speed[0]
    if rect.top < 0 or rect.bottom > window_size[1]:
        rect_speed[1] = -rect_speed[1]

    # 填充背景色
    screen.fill(WHITE)

    # 绘制矩形
    pygame.draw.rect(screen, RED, rect)

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)  # 设置帧率为 60 FPS

# 退出 Pygame
pygame.quit()
