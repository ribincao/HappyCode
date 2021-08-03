import gevent


def task(pid):
    gevent.sleep(0.5)
    print(f"Task {pid} done")


def synchronous():
    for i in range(1, 10):
        task(i)


def asynchronous():
    threads = [gevent.spawn(task, i) for i in range(10)]
    gevent.joinall(threads)


if __name__ == "__main__":
    print("synchronous: ")
    synchronous()

    print("asynchronous")
    asynchronous()