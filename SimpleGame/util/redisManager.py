import redis


class RedisManager:

    def __init__(self, host, port, db):
        self._host = host
        self._port = port
        self._db = db
        self.conn = None

    def connect(self):
        self.conn = redis.StrictRedis(host=self._host, port=self._port, db=self._db)

    def get(self, key: str):
        value = self.conn.get(key)
        if value:
            value = value.decode()
        return value

    def set(self, key: str, value: str):
        self.conn.set(key, value)


r = RedisManager('localhost', 6379, 0)
r.connect()
