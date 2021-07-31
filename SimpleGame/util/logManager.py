import datetime
import os


class LogManager:

    def __init__(self, file_path):
        if os.path.exists(file_path):
            self._file = open(file_path, 'a')
        self._file = open(file_path, 'w')

    def err(self, msg):
        now_date = datetime.datetime.now()
        self._file.write('[' + str(now_date) + '] ' + "ERROR: " + msg + '\r\n')
        self._file.flush()

    def debug(self, msg):
        now_date = datetime.datetime.now()
        self._file.write('[' + str(now_date) + '] ' + "DEBUG: " + msg + '\r\n')
        self._file.flush()

    def info(self, msg):
        now_date = datetime.datetime.now()
        self._file.write('[' + str(now_date) + '] ' + "INFO: " + msg + '\r\n')
        self._file.flush()


now = datetime.datetime.now()
now = str(now)[:10]
log = LogManager("./log/" + now + ".log")

