import pygame  # 导入pygame库，用于字体处理


class FontManager:
    """字体管理类，负责字体加载和管理，确保中文正常显示"""

    def __init__(self):
        """初始化字体管理器，加载不同大小的字体（大/中/小）"""
        try:
            # 尝试加载系统中的中文字体（优先SimHei、微软雅黑， fallback为Arial）
            # 大字体（72号）
            self.font_large = pygame.font.SysFont(
                ["Microsoft YaHei", "SimHei", "Arial"], 72
            )
            # 中字体（40号）
            self.font_medium = pygame.font.SysFont(
                ["Microsoft YaHei", "SimHei", "Arial"], 40
            )
            # 小字体（24号）
            self.font_small = pygame.font.SysFont(
                ["Microsoft YaHei", "SimHei", "Arial"], 24
            )
        except:
            # 若加载失败，使用pygame默认字体
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 24)

    def get_large_font(self):
        """获取大字体（72号）"""
        return self.font_large

    def get_medium_font(self):
        """获取中字体（40号）"""
        return self.font_medium

    def get_small_font(self):
        """获取小字体（24号）"""
        return self.font_small
