import contextlib


@contextlib.contextmanager
def MyOpen(file_path):
    print(f"__enter__: {file_path}")
    file_handler= open(file_path)

    yield file_handler

    print(f"__exit__: {file_path}")
    file_handler.close()
    return


if __name__ == '__main__':
    with MyOpen('./test.txt') as f:
        for line in f:
            print(line)