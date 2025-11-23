import sys
import os

# 路径配置
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(current_dir) if "src" not in current_dir else current_dir
    if src_dir not in sys.path:
        sys.path.append(src_dir)

# 导入控制器
from controller.game_controller import GameController

def main():
    game_controller = GameController()
    game_controller.run()


# 分层次 MVC
if __name__ == "__main__":
    main()
