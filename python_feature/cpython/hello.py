import dis
def hello():
    print("hello world")


def compile():
    dis.dis(hello)


def d1():
    d = {}

def d2():
    d = dict()

def compare():
    print("{} for dict")
    dis.dis(d1)
    print("dict() for dict")
    dis.dis(d2)

if __name__ == '__main__':
    compare()
