import redis

conn_pool = redis.ConnectionPool(host='127.0.0.1')
redis_conn = redis.Redis(connection_pool=conn_pool)

redis_conn.lpush('coro_test', 1)
redis_conn.lpush('coro_test', 2)
redis_conn.lpush('coro_test', 3)
redis_conn.lpush('coro_test', 4)
