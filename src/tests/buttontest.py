import pygame
import sys
import os

# 获取当前文件所在目录的父目录（即 src 目录）
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)  # 假设 tests 与 model 同级，都在 src 下
sys.path.append(src_dir)  # 将 src 目录添加到搜索路径

from model.button import Button


# 示例用法
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("按钮示例")
    clock = pygame.time.Clock()

    
    # 创建按钮实例
    start_btn = Button(
        x=300, y=200, width=200, height=60, text="开始游戏", font_size=36
    )

    quit_btn = Button(
        x=300,
        y=300,
        width=200,
        height=60,
        text="退出",
        font_size=36,
        bg_color=(150, 50, 50),
        hover_color=(180, 70, 70),
        click_color=(120, 30, 30),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))  # 背景色

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 按钮事件检测
            if start_btn.handle_event(event):
                print("开始游戏按钮被点击！")
            if quit_btn.handle_event(event):
                running = False

        # 绘制按钮
        start_btn.draw(screen)
        quit_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
