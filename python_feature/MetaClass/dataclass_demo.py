from typing import List
from dataclasses import dataclass

# 自动生成了 __init__, __eq__ 等方法
@dataclass
class Test:

    name: str
    age: int
    nums: List[int]

    def get_age(self) -> int:
        return self.age


if __name__ == '__main__':
    t1 = Test(name="ribincao", age=26, nums=[1,2])
    t2 = Test(name="ribincao", age=26, nums=[1, 2])
    t3 = Test(name="ribincao", age=27, nums=[1, 2])

    print(t1, t1 == t2, t1 == t3)