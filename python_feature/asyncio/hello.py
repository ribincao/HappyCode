import time

def hello():
    time.sleep(1)

def run():
    for i in range(5):
        hello()
        print(f"{i}: Hello world!")


if __name__ == '__main__':
    run()
