import pygame
import math
import random

from utils.color import ColorPalette


class SnakeAnimation:
    """贪吃蛇动画组件：简单高效、持续移动增长、无头部区分"""

    def __init__(self, color_palette=None):
        """初始化蛇动画"""
        # 初始10段蛇身（默认较长），相对坐标简化
        self.segments = [(0.06 + i * 0.009, 0.5) for i in range(10)]
        self.base_speed = 0.004  # 微调速度，确保移动明显不卡顿
        self.base_size = 12  # 统一蛇身大小
        self.color_palette = color_palette or ColorPalette()
        self.base_color = self.color_palette.get_title_color()

        # 呼吸效果简化（降低计算量）
        self.breath_timer = 0

        # 移动方向：随机初始方向，确保不静止
        self.direction = self._get_random_dir()

        # 增长配置：简单直接，1-2秒增长一次（60-120帧）
        self.max_length = 30
        self.grow_timer = 0
        self.grow_interval = random.randint(60, 120)

        # 边界配置：简化缓冲，避免贴边
        self.border = 0.08
        self.min_x, self.max_x = self.border, 1 - self.border
        self.min_y, self.max_y = self.border, 1 - self.border

    def _get_random_dir(self):
        """简化随机方向生成，确保移动不中断"""
        angle = random.uniform(0, math.pi * 2)  # 随机角度（0-360度）
        return (math.cos(angle) * self.base_speed, math.sin(angle) * self.base_speed)

    def _breath_effect(self):
        """简化呼吸效果，减少计算"""
        self.breath_timer += 0.05
        return 0.95 + math.sin(self.breath_timer) * 0.08  # 缩放范围0.87-1.03

    def _get_segment_color(self, index):
        """简化颜色渐变，提升效率"""
        # 仅轻微调整亮度，减少计算
        darken = index * 2
        return (
            max(0, self.base_color[0] - darken),
            max(0, self.base_color[1] - darken),
            max(0, self.base_color[2] - darken),
            230,  # 固定透明度，避免动态计算
        )

    def update(self, win_width, win_height):
        """简化更新逻辑，确保持续移动"""
        # 1. 持续增长（简单逻辑：计时到就加段）
        self.grow_timer += 1
        if (
            self.grow_timer >= self.grow_interval
            and len(self.segments) < self.max_length
        ):
            self.segments.append(self.segments[-1])  # 直接复制尾部，简化延伸逻辑
            self.grow_timer = 0
            self.grow_interval = random.randint(60, 120)

        # 2. 头部移动（确保不静止）
        head_x, head_y = self.segments[0]
        new_head_x = head_x + self.direction[0]
        new_head_y = head_y + self.direction[1]

        # 3. 边界反弹（简化逻辑，触边即反向，确保移动不中断）
        if new_head_x <= self.min_x or new_head_x >= self.max_x:
            self.direction = (-self.direction[0], self.direction[1])
            new_head_x = max(self.min_x, min(self.max_x, new_head_x))  # 强制回边界内
        if new_head_y <= self.min_y or new_head_y >= self.max_y:
            self.direction = (self.direction[0], -self.direction[1])
            new_head_y = max(self.min_y, min(self.max_y, new_head_y))

        # 4. 更新蛇身（头部插入，尾部移除，确保移动连贯）
        self.segments.insert(0, (new_head_x, new_head_y))
        self.segments.pop()

        # 5. 极低概率随机变向（避免轨迹重复，不频繁）
        if random.random() < 0.008:
            self.direction = self._get_random_dir()

    def draw(self, surface, win_width, win_height):
        """简化绘制逻辑，提升效率"""
        breath_scale = self._breath_effect()
        current_size = int(self.base_size * breath_scale)

        # 正向遍历绘制（简化顺序，不影响视觉）
        for i, (x_ratio, y_ratio) in enumerate(self.segments):
            x = x_ratio * win_width
            y = y_ratio * win_height
            color = self._get_segment_color(i)

            # 绘制蛇身（仅圆形+细边框，减少绘制操作）
            pygame.draw.circle(surface, color, (int(x), int(y)), current_size)
            pygame.draw.circle(
                surface,
                (
                    min(color[0] + 20, 255),
                    min(color[1] + 20, 255),
                    min(color[2] + 20, 255),
                ),
                (int(x), int(y)),
                current_size,
                width=1,
            )
