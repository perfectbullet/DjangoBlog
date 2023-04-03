import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.flushdb()
    r.rpush('employee', 'scott')
    r.rpush('employee', 'jack')
    r.rpush('employee', 'scott')
    r.lrem('employee', 1, 'scott')
    print(r.lrange('employee', 0, -1))
    r.lpush('employee', 'scott')
    r.lrem('employee', 2, 'scott')
    print(r.lrange('employee', 0, -1))