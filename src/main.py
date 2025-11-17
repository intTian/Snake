# main文件 组织各模块协同工作
import pygame
import sys

from controller.single_player import SinglePlayerMode
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT

# 分层次 MVC

"""
当前执行脚本所在的目录（或交互式环境的当前工作目录）。
环境变量 PYTHONPATH 中配置的目录。
Python 标准库的安装目录（如 .../lib/site-packages）。
第三方库的安装目录（如 Conda 环境的 site-packages）。
"""
# # 打印所有搜索路径
# for path in sys.path:
#     print(path)


def main():


    """
    1.模式选择 按钮
    """


    """
    2.单人模式
    """
    
    # 初始化Pygame
    pygame.init()
    # 创建游戏窗口（也叫 “屏幕表面”），用于绘制游戏内容（蛇、食物、文字等）
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 窗口名
    pygame.display.set_caption("贪吃蛇游戏")
    # 建一个时钟对象，用于控制游戏的帧率
    clock = pygame.time.Clock()
    # 字体
    pygame.font.init()
    # 然后再创建字体对象
    font = pygame.font.SysFont(["Microsoft YaHei UI"], 36)

    # 模式选择界面循环
    selecting = True
    # selecting = False
    while selecting:
        # fill() 方法通过 RGB 颜色值 (0,0,0)（黑色）覆盖整个窗口
        screen.fill((0, 0, 0))  # 黑色背景

        # 绘制标题和选项
        # font.render(文字, 抗锯齿, 颜色)将文字转换为可绘制的图像（Surface 对象）。
        # screen.blit(图像, 位置)将生成的文字图像绘制到窗口的指定位置。
        option1 = font.render("1.单人模式", True, (255, 255, 255))
        screen.blit(option1, (SCREEN_WIDTH // 2 - 150, 250))

        option2 = font.render("2.本地对战", True, (100, 100, 100))
        screen.blit(option2, (SCREEN_WIDTH // 2 - 150, 300))

        option3 = font.render("3.联网对战", True, (100, 100, 100))
        screen.blit(option3, (SCREEN_WIDTH // 2 - 150, 350))
        # pygame.display.flip() 刷新整个窗口，将所有绘制的内容（标题、选项）显示到屏幕上。
        pygame.display.flip()
        # 控制模式选择界面的帧率，限制每秒最多刷新 10 次。
        clock.tick(30)

        # 处理模式选择输入
        # 遍历 Pygame 事件队列中的所有事件（如鼠标点击、键盘按键、窗口关闭等）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 关闭 Pygame 所有模块，释放资源。
                return
            # 处理键盘按键按下事件（KEYDOWN）
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # 数字1
                    # 启动单人模式
                    game = SinglePlayerMode()
                    game.run()
                    selecting = False  # 退出选择界面
                elif event.key == pygame.K_ESCAPE:  # ESC 键（pygame.K_ESCAPE）
                    pygame.quit()
                    return


if __name__ == "__main__":
    main()
