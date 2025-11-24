import pygame
import sys
from pygame.locals import *  # type: ignore
from controller.local_controller import LocalController
from controller.single_controller import SingleController
from model.Local_game import LocalGame
from model.single_game import SingleGame
from utils.color import ColorPalette
from utils.font import FontManager
from view.local_view import LocalView
from view.single_view import SingleView
from view.start_view import StartView  # 依赖视图


# 开始控制器
class StartController:
    """游戏控制器：负责逻辑处理（事件、状态、业务）"""

    def __init__(self, width=800, height=600, title="贪吃蛇小游戏"):
        # 初始化工具类
        self.font_manager = FontManager()
        self.color_palette = ColorPalette()

        # 窗口基础配置
        self.width = width
        self.height = height
        self.title = title
        self.running = True

        # 初始化视图（控制器持有视图，通过视图绘制界面）
        self.view = StartView(
            self.width, self.height, self.font_manager, self.color_palette, self.title
        )

        # 游戏状态（可扩展：当前选择的模式、是否暂停等）
        self.current_mode = None

        # 时钟（控制帧率）
        self.clock = pygame.time.Clock()

    def _handle_button_action(self, action):
        """处理按钮点击业务逻辑"""
        # print(f"选择了: {action}")
        self.current_mode = action

        if action == "single":
            model = SingleGame()
            # 2. 创建视图（界面展示）
            view = SingleView(model)
            # 3. 创建控制器（逻辑调度与交互）
            controller = SingleController(model, view)
            # 4. 启动游戏主循环
            controller.run_game()

        elif action == "local":  # 新增人机对战逻辑
            model = LocalGame()
            view = LocalView(model)
            controller = LocalController(model, view)
            controller.run_game()

        elif action == "quit":
            self.running = False

    def handle_events(self):
        """处理所有事件（控制器核心：事件分发+逻辑处理）"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            # 鼠标移动：通知视图更新按钮悬停状态
            elif event.type == MOUSEMOTION:
                self.view.update_button_hover(event.pos)

            # 鼠标点击：获取视图的点击结果，处理业务逻辑
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    clicked_action = self.view.check_button_click(event.pos)
                    if clicked_action:
                        self._handle_button_action(clicked_action)

            # 窗口缩放：更新控制器尺寸，通知视图同步缩放
            elif event.type == VIDEORESIZE:
                self.width, self.height = event.w, event.h
                self.view.resize(self.width, self.height)

    def update(self):
        """更新游戏状态（控制器核心：同步视图状态）"""
        # 通知视图更新动态元素（标题动画、蛇动画、背景）
        self.view.update_animations(self.width, self.height)

    def render(self):
        """触发视图绘制（控制器不绘制，只调用视图绘制方法）"""
        self.view.draw(self.width, self.height)

    def run(self):
        """主循环（控制器驱动：事件→更新→渲染）"""
        while self.running:
            self.handle_events()  # 处理事件（逻辑）
            self.update()  # 更新状态（逻辑）
            self.render()  # 绘制界面（视图）
            self.clock.tick(60)

        # 退出清理
        pygame.quit()
        sys.exit()
