import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("ribincao", "123456")
print(r.get('root'))