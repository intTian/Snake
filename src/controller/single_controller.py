import pygame


class SingleController:
    def __init__(self, model, view):
        # 关联模型（数据逻辑）和视图（界面展示）
        self.model = model
        self.view = view

    def handle_events(self):
        """处理用户输入事件（重点：监听按键按下/松开）"""
        for event in pygame.event.get():
            # 窗口关闭事件：结束游戏
            if event.type == pygame.QUIT:
                self.model.is_running = False

            # 按键按下事件：设置对应速度
            if event.type == pygame.KEYDOWN:
                # 按Q退出游戏
                if event.key == pygame.K_q:
                    self.model.is_running = False
                # 按R重新开始
                elif event.key == pygame.K_r:
                    self.model.reset()

                # 方向键+WASD：设置蛇的移动速度（新增WASD键映射）
                if event.key in [
                    pygame.K_UP,
                    pygame.K_w,  # 上方向（上箭头+W）
                    pygame.K_DOWN,
                    pygame.K_s,  # 下方向（下箭头+S）
                    pygame.K_LEFT,
                    pygame.K_a,  # 左方向（左箭头+A）
                    pygame.K_RIGHT,
                    pygame.K_d,  # 右方向（右箭头+D）
                ]:
                    self.model.set_velocity(event.key, is_pressed=True)

            # 按键松开事件：停止移动（仅当松开的是当前移动方向键时）
            if event.type == pygame.KEYUP:
                if event.key in [
                    pygame.K_UP,
                    pygame.K_w,  # 上方向（上箭头+W）
                    pygame.K_DOWN,
                    pygame.K_s,  # 下方向（下箭头+S）
                    pygame.K_LEFT,
                    pygame.K_a,  # 左方向（左箭头+A）
                    pygame.K_RIGHT,
                    pygame.K_d,  # 右方向（右箭头+D）
                ]:
                    self.model.set_velocity(event.key, is_pressed=False)

    def run_game(self):
        """游戏主循环（调度模型和视图）"""
        # 初始化生成5个食物（满足多食物需求）
        self.model.generate_food(5)
        # 游戏运行中循环
        while self.model.is_running:
            # 1. 处理用户按键输入
            self.handle_events()
            # 2. 控制蛇移动（根据速度向量）
            self.model.move_snake()
            # 3. 更新界面显示
            self.view.update()
        # 游戏结束后关闭窗口
        self.view.quit()
