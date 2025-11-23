import pygame
from controller.single_controller import SingleController


class LocalController(SingleController):
    def run_game(self):
        self.model.generate_food(5)
        while self.model.is_running:
            self.handle_events()
            self.model.move_snake()  # 玩家移动
            self.model.ai_move()  # AI移动
            self.view.update()
        self.view.quit()



