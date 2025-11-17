import pygame
import sys
import math
import random
from pygame.locals import *

# 初始化Pygame
pygame.init()
pygame.font.init()

# 确保中文显示正常
try:
    font_large = pygame.font.SysFont(["SimHei", "Microsoft YaHei", "Arial"], 72)
    font_medium = pygame.font.SysFont(["SimHei", "Microsoft YaHei", "Arial"], 40)
    font_small = pygame.font.SysFont(["SimHei", "Microsoft YaHei", "Arial"], 24)
except:
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 24)

# 屏幕初始设置（支持缩放）
WIDTH, HEIGHT = 800, 600
# 关键：添加RESIZABLE标志允许窗口缩放
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("贪吃蛇游戏")

# --------------------------
# 设置窗口图标（关键代码）
# --------------------------
try:
    # 加载图标图片（替换为你的图标路径，建议32x32或64x64像素）
    icon = pygame.image.load("resource\\snake_icon.ico").convert_alpha()
    # 设置图标
    pygame.display.set_icon(icon)
except:
    # 若图片加载失败，使用默认图标（可选）
    print("警告：未找到图标文件，使用默认图标")


# 颜色定义
BACKGROUND_COLOR = (10, 10, 30)
GRADIENT_COLORS = [(30, 30, 80), (50, 20, 100), (20, 50, 120)]
BUTTON_COLOR = (60, 130, 240)
BUTTON_HOVER_COLOR = (100, 160, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 215, 0)
DESCRIPTION_COLOR = (200, 200, 255)


# 按钮类（适配缩放）
class Button:
    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, text, action=None):
        # 用相对比例定义位置和大小（0-1之间，相对于窗口宽高），方便缩放
        self.x_ratio = x_ratio  # x坐标相对窗口宽度的比例
        self.y_ratio = y_ratio  # y坐标相对窗口高度的比例
        self.width_ratio = width_ratio  # 宽度相对窗口宽度的比例
        self.height_ratio = height_ratio  # 高度相对窗口高度的比例
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR
        self.hover = False
        self.radius = 15
        self.pulse = 0
        # 实时计算的矩形（随窗口缩放更新）
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect(WIDTH, HEIGHT)  # 初始计算

    def update_rect(self, win_width, win_height):
        # 根据窗口当前大小更新按钮位置和尺寸
        self.rect.x = win_width * self.x_ratio
        self.rect.y = win_height * self.y_ratio
        self.rect.width = win_width * self.width_ratio
        self.rect.height = win_height * self.height_ratio

    def draw(self, surface):
        if self.hover:
            self.pulse = (self.pulse + 0.05) % math.pi
            pulse_offset = int(5 * math.sin(self.pulse))
            pulse_rect = self.rect.inflate(pulse_offset, pulse_offset)
            pygame.draw.rect(
                surface,
                (
                    min(255, self.color[0] + 30),
                    min(255, self.color[1] + 30),
                    min(255, self.color[2] + 30),
                ),
                pulse_rect,
                border_radius=self.radius + 2,
            )

        current_color = BUTTON_HOVER_COLOR if self.hover else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.radius)

        text_surf = font_medium.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def click(self, pos):
        return self.rect.collidepoint(pos)


# 创建按钮（用相对比例定义，适配缩放）
buttons = [
    # x_ratio, y_ratio, width_ratio, height_ratio, text, action
    Button(
        0.5 - 0.375 / 2, 0.4, 0.375, 0.1, "单人模式", "single"
    ),  # 0.375=300/800（相对宽度）
    Button(0.5 - 0.375 / 2, 0.55, 0.375, 0.1, "本地对战", "local"),
    Button(0.5 - 0.375 / 2, 0.7, 0.375, 0.1, "联网对战", "online"),
    Button(0.5 - 0.375 / 2, 0.85, 0.375, 0.1, "退出游戏", "quit"),
]


# 贪吃蛇动画类（适配缩放）
class SnakeAnimation:
    def __init__(self):
        self.segments = [
            (0.125, 0.5),
            (0.1, 0.5),
            (0.075, 0.5),
            (0.05, 0.5),
        ]  # 用相对坐标（0-1）
        self.direction = (0.006, 0)  # 相对速度（每秒移动窗口宽度的比例）
        self.color = TITLE_COLOR
        self.speed = 3

    def update(self, win_width, win_height):
        # 根据窗口大小计算实际坐标并移动
        head_x, head_y = self.segments[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.segments.insert(0, new_head)
        self.segments.pop()

        # 边界反弹（相对坐标0-1）
        head_x, head_y = self.segments[0]
        if head_x > 1 or head_x < 0:
            self.direction = (-self.direction[0], self.direction[1])
        if head_y > 1 or head_y < 0:
            self.direction = (self.direction[0], -self.direction[1])

    def draw(self, surface, win_width, win_height):
        # 转换相对坐标为实际像素坐标并绘制
        for i, (x_ratio, y_ratio) in enumerate(self.segments):
            x = x_ratio * win_width
            y = y_ratio * win_height
            size = 15 if i == 0 else max(5, 15 - i // 2)
            pygame.draw.circle(surface, self.color, (int(x), int(y)), size)

            # 头部眼睛
            if i == 0:
                eye_offset_x = 5 * (
                    1 if self.direction[0] > 0 else -1 if self.direction[0] < 0 else 0
                )
                eye_offset_y = 5 * (
                    1 if self.direction[1] > 0 else -1 if self.direction[1] < 0 else 0
                )

                if eye_offset_x != 0:
                    pygame.draw.circle(
                        surface, (0, 0, 0), (int(x) + eye_offset_x, int(y) - 3), 3
                    )
                    pygame.draw.circle(
                        surface, (0, 0, 0), (int(x) + eye_offset_x, int(y) + 3), 3
                    )
                else:
                    pygame.draw.circle(
                        surface, (0, 0, 0), (int(x) - 3, int(y) + eye_offset_y), 3
                    )
                    pygame.draw.circle(
                        surface, (0, 0, 0), (int(x) + 3, int(y) + eye_offset_y), 3
                    )


snake_anim = SnakeAnimation()


# 背景星星类（适配缩放）
class Star:
    def __init__(self):
        self.x_ratio = random.random()  # 相对x坐标（0-1）
        self.y_ratio = random.random()  # 相对y坐标（0-1）
        self.size = random.uniform(1, 3)
        self.brightness = random.uniform(0.3, 1)
        self.pulse_speed = random.uniform(0.01, 0.03)
        self.pulse_dir = 1

    def update(self):
        self.brightness += self.pulse_speed * self.pulse_dir
        if self.brightness > 1:
            self.brightness = 1
            self.pulse_dir = -1
        elif self.brightness < 0.3:
            self.brightness = 0.3
            self.pulse_dir = 1

    def draw(self, surface, win_width, win_height):
        x = self.x_ratio * win_width
        y = self.y_ratio * win_height
        color = (
            int(255 * self.brightness),
            int(255 * self.brightness),
            int(255 * self.brightness),
        )
        pygame.draw.circle(surface, color, (int(x), int(y)), int(self.size))


stars = [Star() for _ in range(100)]


# 主循环
clock = pygame.time.Clock()
running = True
current_width, current_height = WIDTH, HEIGHT  # 记录当前窗口大小
title_oscillation = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            # 检查按钮悬停
            for button in buttons:
                button.check_hover(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    if button.click(event.pos) and button.action:
                        print(f"选择了: {button.action}")
                        if button.action == "quit":
                            running = False
        # --------------------------
        # 窗口缩放事件处理（关键代码）
        # --------------------------
        elif event.type == VIDEORESIZE:
            # 更新当前窗口大小
            current_width, current_height = event.w, event.h
            # 调整按钮位置和尺寸
            for button in buttons:
                button.update_rect(current_width, current_height)

    # 更新动画元素
    title_oscillation += 0.05
    # 标题位置随窗口高度动态调整（相对高度0.15）
    title_y = current_height * 0.15 + math.sin(title_oscillation) * 5

    # 蛇动画随窗口大小更新
    snake_anim.update(current_width, current_height)

    for star in stars:
        star.update()

    # 绘制背景
    screen.fill(BACKGROUND_COLOR)

    # 绘制渐变背景（适配当前窗口高度）
    for i in range(current_height):
        ratio = i / current_height
        if ratio < 0.33:
            color = (
                int(
                    GRADIENT_COLORS[0][0] * (1 - ratio * 3)
                    + GRADIENT_COLORS[1][0] * (ratio * 3)
                ),
                int(
                    GRADIENT_COLORS[0][1] * (1 - ratio * 3)
                    + GRADIENT_COLORS[1][1] * (ratio * 3)
                ),
                int(
                    GRADIENT_COLORS[0][2] * (1 - ratio * 3)
                    + GRADIENT_COLORS[1][2] * (ratio * 3)
                ),
            )
        else:
            ratio2 = (ratio - 0.33) / 0.67
            color = (
                int(
                    GRADIENT_COLORS[1][0] * (1 - ratio2)
                    + GRADIENT_COLORS[2][0] * ratio2
                ),
                int(
                    GRADIENT_COLORS[1][1] * (1 - ratio2)
                    + GRADIENT_COLORS[2][1] * ratio2
                ),
                int(
                    GRADIENT_COLORS[1][2] * (1 - ratio2)
                    + GRADIENT_COLORS[2][2] * ratio2
                ),
            )
        pygame.draw.line(screen, color, (0, i), (current_width, i))

    # 绘制星星
    for star in stars:
        star.draw(screen, current_width, current_height)

    # 绘制标题（适配窗口宽度居中）
    title_text = font_large.render("贪吃蛇大作战", True, TITLE_COLOR)
    title_shadow = font_large.render("贪吃蛇大作战", True, (100, 100, 100))
    # 标题x坐标：窗口中心 - 文本宽度的一半
    title_x = current_width // 2 - title_text.get_width() // 2
    screen.blit(title_shadow, (title_x + 2, title_y + 2))
    screen.blit(title_text, (title_x, title_y))

    # 绘制副标题（随标题位置动态调整）
    subtitle = font_small.render("经典游戏 · 全新体验", True, DESCRIPTION_COLOR)
    subtitle_x = current_width // 2 - subtitle.get_width() // 2
    screen.blit(subtitle, (subtitle_x, title_y + 80))

    # 绘制动画蛇
    snake_anim.draw(screen, current_width, current_height)

    # 绘制按钮
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
