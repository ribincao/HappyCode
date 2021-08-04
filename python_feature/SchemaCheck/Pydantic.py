from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


def demo():
    p = Person(name="ribincao", age="26")
    print(p.json())

    t = {"name": "Tom", "age": 27}
    t = Person(**t)
    print(t.json())


if __name__ == '__main__':
    demo()
