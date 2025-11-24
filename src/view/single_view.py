import pygame
import os 
import sys

class SingleView:
    """贪吃蛇游戏视图类，负责界面绘制与显示"""

    def __init__(self, model):
        self.model = model
        self.cell_size = 20
        self.is_initialized = False
        self._init_pygame()  # 简化方法名

        # 颜色配置（精简键名和注释）
        self.colors = {
            "snake": (0, 255, 0),
            "snake_head": (0, 200, 0),
            "food": (255, 0, 0),
            "bg": (0, 0, 0),
            "text": (255, 255, 255),
            "border": (50, 50, 50),
            "game_over_bg": (0, 0, 0, 180),
        }

        # 字体与时钟（合并初始化）
        self.font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 25)
        self.clock = pygame.time.Clock()
        self.fps = 15

    def _init_pygame(self):
        """初始化Pygame和窗口"""
        if not pygame.get_init():
            pygame.init()
        # 计算窗口尺寸并创建窗口（合并代码）
        w = (self.model.config.border_x[1] + 1) * self.cell_size
        h = (self.model.config.border_y[1] + 1) * self.cell_size
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("贪吃蛇小游戏")
        # icon
        self._set_icon()
        self.is_initialized = True


    def get_resource_path(self, relative_path):
        if getattr(sys, "frozen", False):
            # 打包后环境
            base_path = sys._MEIPASS  # type: ignore
        else:
            # 开发环境：根据当前文件位置定位到项目根目录下的resource
            # 假设当前类文件在src/view/目录下，需要回退到src目录再找resource
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _set_icon(self):
        """设置窗口图标（视图负责UI相关配置）"""
        try:
            # 使用get_resource_path获取正确路径，自动适配开发/打包环境
            icon_path = self.get_resource_path("resource/snake_icon.ico")
            # 加载图片时使用获取到的路径，而非硬编码路径
            icon = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"警告：未找到图标文件，使用默认图标。错误：{e}")

    def draw_border(self):
        """绘制边框"""
        w = (self.model.config.border_x[1] + 1) * self.cell_size
        h = (self.model.config.border_y[1] + 1) * self.cell_size
        pygame.draw.rect(self.screen, self.colors["border"], (0, 0, w, h), 2)

    def draw_snake(self):
        """绘制蛇（带渐变和方向指示）"""
        if not self.model.snake:
            return
        # 蛇身颜色渐变（从头部到尾部逐渐变浅）
        total_segments = len(self.model.snake)
        head_x, head_y = self.model.snake[0]

        # 头部（增加方向指示三角形）
        head_color = self.colors["snake_head"]
        pygame.draw.rect(
            self.screen,
            head_color,
            (
                head_x * self.cell_size,
                head_y * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1,
            ),
            border_radius=6,  # 头部圆角更大
        )
        # 绘制方向箭头（小三角形）
        dir_x, dir_y = (
            self.model.velocity
            if self.model.velocity != (0, 0)
            else self.model.last_velocity
        )
        arrow_size = self.cell_size // 3
        arrow_points = [
            (
                head_x * self.cell_size + self.cell_size // 2,
                head_y * self.cell_size + self.cell_size // 2,
            ),
            (
                head_x * self.cell_size + self.cell_size // 2 - dir_x * arrow_size,
                head_y * self.cell_size + self.cell_size // 2 - dir_y * arrow_size,
            ),
            (
                head_x * self.cell_size
                + self.cell_size // 2
                - dir_x * arrow_size // 2
                + dir_y * arrow_size // 2,
                head_y * self.cell_size
                + self.cell_size // 2
                - dir_y * arrow_size // 2
                - dir_x * arrow_size // 2,
            ),
        ]
        pygame.draw.polygon(self.screen, (0, 150, 0), arrow_points)  # 深绿色箭头

        # 身体（颜色渐变）
        for i, (x, y) in enumerate(self.model.snake[1:]):
            # 从头部到尾部，绿色值逐渐降低（0-255 → 100-200）
            green = 200 - int(100 * (i / total_segments))
            body_color = (0, green, 0)
            pygame.draw.rect(
                self.screen,
                body_color,
                (
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1,
                ),
                border_radius=3,
            )

    def draw_foods(self):
        """绘制带发光效果的彩色食物"""
        cs = self.cell_size
        for i, (x, y) in enumerate(self.model.foods):
            # 随机食物颜色（红、黄、紫等鲜艳色）
            food_colors = [
                (255, 50, 50),
                (255, 255, 50),
                (200, 50, 200),
                (50, 200, 255),
            ]
            color = food_colors[i % len(food_colors)]

            # 发光外框（比食物大一点，半透明）
            glow_radius = cs // 2 + 2
            glow_surface = pygame.Surface(
                (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surface,
                (*color, 80),  # 半透明发光效果
                (glow_radius, glow_radius),
                glow_radius,
            )
            self.screen.blit(
                glow_surface,
                (x * cs + cs // 2 - glow_radius, y * cs + cs // 2 - glow_radius),
            )

            # 食物本体（圆形）
            pygame.draw.circle(
                self.screen,
                color,
                (x * cs + cs // 2, y * cs + cs // 2),
                cs // 2 - 1,
            )

    def draw_score(self):
        """绘制分数"""
        score = max(0, len(self.model.snake) - 3)
        self.screen.blit(
            self.font.render(f"分数: {score}", True, self.colors["text"]), (10, 10)
        )

    def draw_game_over(self):
        """绘制精美的游戏结束界面"""
        # 半透明全屏遮罩
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # 更暗的遮罩（alpha=200）
        self.screen.blit(overlay, (0, 0))

        # 标题文字（更大字号）
        title_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei"], 40)
        title_text = title_font.render("游戏结束", True, (255, 80, 80))
        title_rect = title_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40)
        )
        self.screen.blit(title_text, title_rect)

        # 分数展示
        score = max(0, len(self.model.snake) - 3)
        score_text = self.font.render(f"最终分数: {score}", True, self.colors["text"])
        score_rect = score_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(score_text, score_rect)

        # 操作提示
        hint_text = self.font.render("按Q退出 | 按R重新开始", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40)
        )
        self.screen.blit(hint_text, hint_rect)

    def draw_background(self):
        """绘制渐变背景+网格线"""
        # 1. 垂直渐变背景（从深黑到纯黑）
        w, h = self.screen.get_size()
        for y in range(h):
            # 渐变比例：顶部偏暗，底部纯黑
            shade = int(20 * (1 - y / h))  # 0-20的灰度值
            color = (shade, shade, shade)
            pygame.draw.line(self.screen, color, (0, y), (w, y))

        # 2. 浅色网格线（间隔cell_size）
        grid_color = (30, 30, 30)  # 深灰色网格
        # 横线
        for y in range(0, h, self.cell_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (w, y), 1)
        # 竖线
        for x in range(0, w, self.cell_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, h), 1)

    def update(self):
        """更新游戏界面"""
        self.draw_background()  # 替换原来的 screen.fill
        # 批量调用绘制方法（保持不变）
        for func in [
            self.draw_border,
            self.draw_snake,
            self.draw_foods,
            self.draw_score,
        ]:
            func()
        # 游戏结束提示（合并判断条件）
        if not self.model.is_running or self.model.game_over:
            self.draw_game_over()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        """退出游戏"""
        if self.is_initialized:
            # pygame.quit()
            self.is_initialized = False
