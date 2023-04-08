from redis_db import pool
import redis
import time

con = redis.Redis(
    connection_pool=pool
)

con.set('country', '英国')
con.set('city', '伦敦')
# city = con.get('city').decode('utf-8')
con.expire('city', 5)
time.sleep(6)
city = con.get('city').decode('utf-8')
print(city)  # 没有这条记录

del con
