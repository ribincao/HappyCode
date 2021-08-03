from greenlet import greenlet


def cor_1():
    print("coroutine 1")
    gr2.switch("hello")
    print("again 1")
    gr2.switch("world")


def cor_2(s):
    print("coroutine 2")
    print(s)
    gr1.switch()
    print("again 2")
    print(s)


if __name__ == '__main__':
    gr1 = greenlet(cor_1)
    gr2 = greenlet(cor_2)
    gr1.switch()
