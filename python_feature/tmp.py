from typing import Any
import pickle
import lz4.frame

THRESHOLD = 10
COMPRESSED = b'1'
UNCOMPRESSED = b'0'

def hello(*args, **kwargs):
    raw_args = pickle_dumps((args, kwargs))
    print(raw_args)


def pickle_dumps(o: Any):
    print(o)
    array = pickle.dumps(o, protocol=pickle.HIGHEST_PROTOCOL)
    compressed = UNCOMPRESSED + array
    print(array, compressed)
    if len(array) > THRESHOLD:
        compressed = lz4.frame.compress(array)
        print(compressed)
        if len(compressed) < len(array):
            compressed = COMPRESSED + compressed
    return compressed


if __name__ == '__main__':
    hello(1, '2', '2', '2', '2', '2', '2', '2')
