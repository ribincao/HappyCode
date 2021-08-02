import threading, time
cancel_timer = False


def work():
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def heart_beat():
    # print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    if not cancel_timer:
        work()
        threading.Timer(3, work).start()


if __name__ == '__main__':
    heart_beat()
    time.sleep(5)
    cancel_timer = True
