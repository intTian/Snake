# 窗口配置
SCREEN_WIDTH = 800  # 窗口宽度（像素）
SCREEN_HEIGHT = 600  # 窗口高度
FPS = 10  # 基础帧率（控制蛇移动速度）

# 游戏元素配置
GRID_SIZE = 20  # 网格大小（蛇身/食物的单位尺寸，需整除窗口尺寸）
SNAKE_INIT_LEN = 3  # 蛇初始长度
SNAKE_COLOR = (0, 255, 0)  # 蛇身颜色（绿色）
FOOD_COLOR = (255, 0, 0)  # 食物颜色（红色）
AI_SNAKE_COLOR = (0, 0, 255)  # AI 蛇颜色（蓝色）
BACKGROUND_COLOR = (0, 0, 0)  # 背景色（黑色）

# 分数配置
FOOD_SCORE = 10  # 吃一个食物得分

# 按键配置
KEY_UP = (119, 273)    # W 键 + 方向上键
KEY_DOWN = (115, 274)  # S 键 + 方向下键
KEY_LEFT = (97, 276)   # A 键 + 方向左键
KEY_RIGHT = (100, 275) # D 键 + 方向右键
KEY_PAUSE = 112        # P 键暂停
KEY_RESTART = 114      # R 键重启
KEY_HELP = 104         # H 键帮助

# 联网配置
SERVER_IP = "0.0.0.0"  # 服务器监听所有网卡
SERVER_PORT = 8888     # 端口号（确保未被占用）
BUFFER_SIZE = 1024     # 数据传输缓冲区大小