"""
文件名：文件名要以test_开头或结尾 例如：test_login.py
函数名：函数名要以test_开头，这样子有助与python自动取搜索他
如果使用类来组织测试，类名应以 Test 开头，并且不应继承自任何特定的基类（除非是为了使用某些特性）


pytest运行中命令行运行可选参数
参数	功能
-v	增加输出的详细程度
-q	减少输出信息
-k EXPRESSION	根据表达式选择运行哪些测试，例如 -k ‘not slow’ 可以跳过标记为 slow 的测试
-x	遇到第一个失败就退出
–html=REPORT.html	生成HTML格式的测试报告，需要安装 pytest-html 插件
–maxfail=NUM	在达到指定数量的失败后停止测试
-m MARKEXPR	只运行带有指定标记的测试，例如 -m slow
-n NUM 或 --numprocesses=NUM	使用多个进程并行运行测试，需要安装 pytest-xdist 插件
-s	不捕获标准输出和错误输出，允许直接看到 print 调用的结果
–ignore=path	忽略指定路径下的测试文件
"""


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5  # 断言


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")  # 断言x是否具有名为check的属性或方法


class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
