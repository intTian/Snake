贪吃蛇游戏
=====

一个基于Pygame的贪吃蛇游戏，包含单人模式和人机对战模式，具有精美的界面和流畅的游戏体验。
功能特点

----

* 两种游戏模式：单人模式、人机对战

* 精美的视觉效果：渐变背景、星星动画、蛇身渐变

* 游戏机制：分数计算、碰撞检测、食物随机生成

* 响应式界面：支持窗口缩放，适配不同屏幕尺寸

项目结构
----

    src/├── main.py               # 程序入口├── controller/           # 控制器模块（游戏逻辑）├── model/                # 模型模块（数据与游戏规则）├── view/                 # 视图模块（界面绘制）├── lib/ui/               # UI组件库（按钮、标题、动画等）├── utils/                # 工具类（颜色、字体管理）└── tests/                # 测试代码

运行说明
----

### 环境依赖

* Python 3.x

* Pygame库

安装依赖：
    pip install pygame

### 启动游戏

    python src/main.py

游戏操作
----

* 方向键：控制蛇移动方向

* 单人模式：吃到食物得分，撞到边界或自身游戏结束

* 人机对战：与AI蛇竞争，撞到AI蛇也会结束游戏

* 游戏结束后：按R重新开始，按Q退出

打包说明
----

如需打包为exe文件，可使用PyInstaller：
    pyinstaller --onefile --noconsole --name 贪吃蛇游戏 --paths=src --add-data "src/resource/*;resource" src/main.py

生成的exe文件位于`dist`目录下。



Windows 系统（图标文件为 .ico 格式）

pyinstaller --onefile --noconsole --name Snake --paths=src --add-data "src/resource/*;resource" --icon=src/resource/snake_icon.ico src/main.py

  

pyinstaller --onefile --noconsole --name Snake  --paths=src  --add-data "src/resource/*;resource"   --icon=src/resource/snake_icon.ico   --upx-dir="D:\Developtools\upx-5.0.2-win64"   src/main.py\

###  新建虚拟环境打包

1. **执行激活命令**：在打开的 cmd 中，输入以下命令（无需额外配置，直接执行）：
   cmd
      pipenv shell

2. **验证是否激活成功**：
   
   * 若 cmd 命令行前面出现 `(项目名-随机字符串)` 的标识（比如 `(Snake-YqVKRRMe)`），说明激活成功；
   * 此时你在 cmd 中执行的 `python`、`pip` 等命令，都指向这个虚拟环境（纯净环境，仅包含之前安装的依赖）。

工具 1：`pipreqs`（精准扫描，优先推荐）

1. 确保在虚拟环境中（cmd 前有`(Snake-xxxx)`标识）；

2. 安装`pipreqs`工具：
   cmd
      pipenv install pipreqs

3. 执行扫描命令（在程序所在文件夹的 cmd 中）：
   cmd
      pipreqs . --encoding=utf8
* 解释：`.` 表示扫描当前文件夹下所有 Python 文件，`--encoding=utf8` 避免中文注释报错；
  4. 扫描完成后，当前文件夹会生成一个 `requirements.txt` 文件，打开后就是程序必需的第三方依赖（一行一个）。


