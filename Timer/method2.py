import threading, time


cnt = 0


def work():
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def heart_beat():
    global cnt
    cnt += 1
    if cnt < 15:
        work()
        threading.Timer(3, work).start()


if __name__ == '__main__':
    heart_beat()
