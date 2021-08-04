from typing import *


def add(num1: int, num2: int) -> int:
    return num1 + num2


if __name__ == '__main__':
    a = '1'
    
    # 实际并不改变类型, 只在静态类型检查的时候生效, 在使用 . 的时候能查找到目标转换类型的方法, 很方便
    # 动态类型检查还是过不了检查, 因为 cast 并没有真正改变其类型
    a = cast(int, a)
    b = 1
    print(add(a, b))
