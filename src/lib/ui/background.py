import sys
import pygame

from lib.ui.star import Star
from utils.color import ColorPalette  # 导入pygame库，用于图形绘制


class StartBackground:
    """背景组件，负责绘制渐变背景和星星"""

    def __init__(self, color_palette=None):
        """初始化背景
        :param color_palette: 颜色管理器实例，默认为None时使用默认颜色配置
        """
        # 初始化颜色管理器，若未传入则使用默认实例
        self.color_palette = color_palette or ColorPalette()
        # 创建100个星星实例，用于背景星空效果
        self.stars = [Star() for _ in range(100)]

    def update(self):
        """更新背景元素（星星闪烁）"""
        # 遍历所有星星，调用其update方法更新闪烁状态
        for star in self.stars:
            star.update()

    def draw(self, surface, win_width, win_height):
        """绘制背景
        :param surface: 绘制表面（pygame的Surface对象）
        :param win_width: 窗口宽度
        :param win_height: 窗口高度
        """
        # 获取渐变颜色列表（从颜色管理器中）
        gradient_colors = self.color_palette.get_gradient_colors()

        # 逐行绘制渐变背景（垂直方向渐变）
        for i in range(win_height):
            # 计算当前行在整个窗口高度中的比例（0-1）
            ratio = i / win_height

            # 前1/3高度：从第一种颜色过渡到第二种颜色
            if ratio < 0.33:
                # 计算过渡比例（0-1），对应0到1/3窗口高度
                transition = ratio * 3
                # 计算当前行的颜色（RGB三通道分别插值）
                color = (
                    int(
                        gradient_colors[0][0] * (1 - transition)
                        + gradient_colors[1][0] * transition
                    ),
                    int(
                        gradient_colors[0][1] * (1 - transition)
                        + gradient_colors[1][1] * transition
                    ),
                    int(
                        gradient_colors[0][2] * (1 - transition)
                        + gradient_colors[1][2] * transition
                    ),
                )
            # 后2/3高度：从第二种颜色过渡到第三种颜色
            else:
                # 计算过渡比例（0-1），对应1/3到1窗口高度
                transition = (ratio - 0.33) / 0.67
                # 计算当前行的颜色（RGB三通道分别插值）
                color = (
                    int(
                        gradient_colors[1][0] * (1 - transition)
                        + gradient_colors[2][0] * transition
                    ),
                    int(
                        gradient_colors[1][1] * (1 - transition)
                        + gradient_colors[2][1] * transition
                    ),
                    int(
                        gradient_colors[1][2] * (1 - transition)
                        + gradient_colors[2][2] * transition
                    ),
                )
            # 绘制当前行（从窗口左侧到右侧的水平线）
            pygame.draw.line(surface, color, (0, i), (win_width, i))

        # 绘制所有星星
        for star in self.stars:
            star.draw(surface, win_width, win_height)
