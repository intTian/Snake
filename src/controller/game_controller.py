import pygame
from controller.start_controller import StartController

# 游戏控制器
class GameController:
    def run(self):
        # 初始化pygame组件
        pygame.init()
        # 初始化控制器，启动游戏
        start_controller = StartController(width=800, height=600, title="贪吃蛇小游戏")
        start_controller.run()
