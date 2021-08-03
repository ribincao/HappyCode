import stackless


def print_x(x):
    print(x)


def tasklet_demo():
    """ 微进程 tasklet """
    # 排队
    stackless.tasklet(print_x)('one')
    stackless.tasklet(print_x)('two')
    stackless.tasklet(print_x)('three')
    # 运行
    stackless.run()


def print_y(y):
    print(f"1: {y}")
    # 遇到 schedule , 当前 tasklet 将暂停, 并将自身重新插入到调度器队列的末尾
    stackless.schedule()
    print(f"2: {y}")
    stackless.schedule()
    print(f"3: {y}")
    stackless.schedule()


def schedule_demo():
    stackless.tasklet(print_y)('first')
    stackless.tasklet(print_y)('second')
    stackless.tasklet(print_y)('third')

    stackless.run()


chan = stackless.channel()


def recv_tasklet():
    print("recv start")
    # 微进程阻塞, 仅当 channel 有消息才会立即恢复执行, 发送信息的微进程则被转移到调度列表的末尾
    # 相反, 如果没有微进程接收消息, send 也会阻塞
    print(chan.receive())
    print("recv finish")


def send_tasklet():
    print("send start")
    chan.send("hello world")
    print("send finish")


def another_tasklet():
    print("another tasklet")


def channel_demo():
    stackless.tasklet(recv_tasklet)()
    stackless.tasklet(send_tasklet)()
    stackless.tasklet(another_tasklet)()

    stackless.run()


ping_channel = stackless.channel()
pong_channel = stackless.channel()


def ping_tasklet():
    while ping_channel.receive():
        print("ping")
        pong_channel.send("ping")


def pong_tasklet():
    while pong_channel.receive():
        print("pong")
        ping_channel.send("pong")


def ping_pong_demo():
    stackless.tasklet(ping_tasklet)()
    stackless.tasklet(pong_tasklet)()

    stackless.tasklet(ping_channel.send)("startup")
    stackless.run()


if __name__ == '__main__':
    ping_pong_demo()
