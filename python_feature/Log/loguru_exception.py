import os
import sys

from loguru import logger

logger.add(os.path.expanduser("./exception_log.log"), backtrace=True, diagnose=True)

def func(a, b):
    return a / b

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")

if __name__ == "__main__":
    nested(0)