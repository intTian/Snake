# 获取当前文件所在目录的父目录（即 src 目录）
import os
import sys
import pygame


class Tests:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)  # 获取src目录
        # 确保src目录只被添加一次
        if src_dir not in sys.path:
            sys.path.append(src_dir)

    def test_star(self):
        """测试Star星星组件的初始化、更新和绘制功能"""

        # 初始化pygame
        pygame.init()
        # 设置测试窗口
        win_width, win_height = 800, 600
        screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Star Component Test")
        clock = pygame.time.Clock()

        # 创建星星列表（生成100颗星星模拟星空）
        stars = [Star() for _ in range(100)]

        # 测试主循环
        running = True
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # 按空格键添加新星星
                    elif event.key == pygame.K_SPACE:
                        stars.append(Star())
                        print(f"新增星星，当前总数：{len(stars)}")

            # 清屏（黑色背景模拟太空）
            screen.fill((0, 0, 0))

            # 更新并绘制所有星星
            for star in stars:
                star.update()  # 更新闪烁状态
                star.draw(screen, win_width, win_height)  # 绘制星星

            # 显示操作提示
            font = pygame.font.SysFont("Microsoft YaHei", 24)
            # font.render()：将文本字符串转换为 Pygame 可绘制的图像（Surface 对象）
            hint = font.render("按ESC退出 | 按空格键添加星星", True, (200, 200, 200))
            screen.blit(hint, (10, 10))

            # 刷新屏幕
            pygame.display.flip()
            # 控制帧率
            clock.tick(60)

        # 退出测试
        pygame.quit()
        sys.exit()

    def test_backgroud(self):
        """测试StartBackground背景组件的初始化、更新和绘制功能"""
        # 初始化pygame
        pygame.init()
        # 设置测试窗口尺寸
        win_width, win_height = 800, 600
        screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("StartBackground Test")
        clock = pygame.time.Clock()

        # 自定义测试用颜色渐变（可选：覆盖默认颜色配置）
        class TestColorPalette(ColorPalette):
            def get_gradient_colors(self):
                # 返回测试用的渐变颜色（顶部深蓝→中间蓝→底部浅蓝）
                return [(10, 10, 50), (30, 30, 100), (60, 60, 150)]

        # 初始化背景组件（使用自定义颜色配置）
        background = StartBackground(color_palette=TestColorPalette())

        # 测试主循环
        running = True
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # 按空格键增加星星
                    elif event.key == pygame.K_SPACE:
                        background.stars.append(Star())  # 需要导入Star类
                        print(f"星星数量: {len(background.stars)}")

            # 更新背景元素（星星闪烁）
            background.update()

            # 绘制背景（渐变+星星）
            background.draw(screen, win_width, win_height)

            # 显示操作提示
            font = pygame.font.SysFont(None, 24)
            hint = font.render("ESC退出 | 空格添加星星", True, (255, 255, 255))
            screen.blit(hint, (10, 10))

            # 刷新屏幕
            pygame.display.flip()
            # 控制帧率
            clock.tick(60)

        # 退出测试
        pygame.quit()
        sys.exit()

    def test_text(self):
        """测试Title标题组件的初始化、更新和绘制功能"""

        # 初始化pygame
        pygame.init()
        # 设置测试窗口
        win_width, win_height = 800, 600
        screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Title Component Test")
        clock = pygame.time.Clock()

        # 创建测试用的颜色和字体管理器
        color_palette = ColorPalette()
        font_manager = FontManager()  # 假设已正确配置字体加载

        # 初始化标题组件
        test_title = Title(
            main_text="测试主标题",
            sub_text="这是一个副标题示例",
            font_manager=font_manager,
            color_palette=color_palette,
        )

        # 测试主循环
        running = True
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # 清屏（使用背景色）
            screen.fill(color_palette.get_background_color())

            # 更新标题动画
            test_title.update()

            # 绘制标题
            test_title.draw(screen, win_width, win_height)

            # 刷新屏幕
            pygame.display.flip()
            # 控制帧率
            clock.tick(60)

        # 退出测试
        pygame.quit()
        sys.exit()

    def test_button(self):
        # 初始化pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("按钮示例")
        clock = pygame.time.Clock()  # 用于控制帧率

        # 按钮点击事件处理函数
        def on_click():
            print("按钮被点击了！")

        # 创建按钮实例
        button = Button(
            x_ratio=0.5,  # x坐标占窗口宽度的50%
            y_ratio=0.5,  # y坐标占窗口高度的50%
            width_ratio=0.2,  # 宽度占窗口宽度的20%
            height_ratio=0.1,  # 高度占窗口高度的10%
            text="点击我",
            action=on_click,
        )

        # 主循环
        running = True
        while running:

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # 处理鼠标点击事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if button.is_clicked(event.pos):
                            # 执行按钮绑定的事件
                            action = button.get_action()
                            if action:
                                action()

            # 清屏（使用深色背景）
            screen.fill((30, 30, 30))

            # 更新按钮状态
            button.update_rect(
                800, 600
            )  # 根据窗口大小更新按钮位置（窗口大小固定时可放循环外）
            button.check_hover(pygame.mouse.get_pos())  # 检测鼠标是否悬停

            # 绘制按钮
            button.draw(screen)

            # 刷新屏幕
            pygame.display.flip()

            # 控制帧率
            clock.tick(60)

        # 退出程序
        pygame.quit()


# 使用
if __name__ == "__main__":
    tests = Tests()

    # 导入包
    from lib.ui.button import Button
    from lib.ui.title import Title
    from utils.color import ColorPalette
    from utils.font import FontManager
    from lib.ui.star import Star
    from lib.ui.background import StartBackground

    # tests.test_button()
    # tests.test_text()
    # tests.test_star()
    # tests.test_backgroud()

