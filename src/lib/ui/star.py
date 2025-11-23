import random  # 导入随机库，用于星星属性随机化
import pygame  # 导入pygame库，用于图形绘制


class Star:
    """星星背景元素组件，用于绘制闪烁的星星效果"""

    def __init__(self):
        """初始化星星（随机属性）"""
        self.x_ratio = random.random()  # 随机x坐标比例（0-1，相对窗口宽度）
        self.y_ratio = random.random()  # 随机y坐标比例（0-1，相对窗口高度）
        self.size = random.uniform(1, 3)  # 随机大小（1-3像素）
        self.brightness = random.uniform(0.3, 1)  # 随机初始亮度（0.3-1）
        self.pulse_speed = random.uniform(0.01, 0.03)  # 随机闪烁速度（0.01-0.03/帧）
        self.pulse_dir = 1  # 闪烁方向（1=变亮，-1=变暗）

    def update(self):
        """更新星星亮度（闪烁效果）"""
        # 根据速度和方向更新亮度
        self.brightness += self.pulse_speed * self.pulse_dir
        # 亮度上限处理（超过1则开始变暗）
        if self.brightness > 1:
            self.brightness = 1
            self.pulse_dir = -1
        # 亮度下限处理（低于0.3则开始变亮）
        elif self.brightness < 0.3:
            self.brightness = 0.3
            self.pulse_dir = 1

    def draw(self, surface, win_width, win_height):
        """绘制星星
        :param surface: 绘制表面（pygame的Surface对象）
        :param win_width: 窗口宽度
        :param win_height: 窗口高度
        """
        # 计算实际坐标（相对比例 * 窗口尺寸）
        x = self.x_ratio * win_width
        y = self.y_ratio * win_height
        # 根据亮度计算颜色（白色系，亮度控制明暗）
        color = (
            int(255 * self.brightness),  # R通道
            int(255 * self.brightness),  # G通道
            int(255 * self.brightness),  # B通道
        )
        # 绘制圆形星星
        pygame.draw.circle(surface, color, (int(x), int(y)), int(self.size))
