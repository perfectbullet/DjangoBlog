import redis
import random
from redis_db import pool

con = redis.Redis(
    connection_pool=pool
)

try:
    con.delete('ballot')
    con.zadd('ballot', {'马云': 0, '丁磊': 0, '张朝阳': 0, '马化腾': 0, '李彦宏': 0})
    names = ['马云', '丁磊', '张朝阳', '马化腾', '李彦宏']
    for i in range(0, 300):
        num = random.randint(0, 4)
        name = names[num]
        con.zincrby('ballot', 1, name)
    result = con.zrevrange('ballot', 0, -1, 'WITHSCORES')
    for one in result:
        print(one[0].decode('utf-8'), int(one[1]))
except Exception as e:
    print(e)
finally:
    del con
