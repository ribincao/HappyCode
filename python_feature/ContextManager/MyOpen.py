class MyOpen:
    
    def __init__(self, path):
        self.file = path
        self.file_handle = None

    def __enter__(self):
        print(f"__enter__: {self.file}")
        self.file_handle = open(self.file)
        return self.file_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 如果出现异常则对 exc_type, exc_val, exc_tb 进行赋值
        print(f"__exit__: {exc_type}, {exc_val}, {exc_tb}")
        if self.file_handle:
            self.file_handle.close()
        # True - 异常被忽视，相当于进行了try-except
        # False - 该异常会被重新raise
        return True


if __name__ == '__main__':
    with MyOpen('./test.txt') as f:
        for line in f:
            print(line)
        raise ZeroDivisionError
