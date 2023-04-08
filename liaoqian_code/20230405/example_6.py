import redis
from redis_db import pool

con = redis.Redis(
    connection_pool=pool
)

try:
    pipline = con.pipeline()
    pipline.watch('9527')
    pipline.multi()
    pipline.hset('9527', 'name', 'jack')
    pipline.hset('9527', 'age', 23)
    pipline.execute()
except Exception as e:
    print(e)
finally:
    if 'pipline' in dir():
        pipline.reset()
    del con
