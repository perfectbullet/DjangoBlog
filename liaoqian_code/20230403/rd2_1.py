import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.flushdb()
    r.hset(8000, 'ename', 'tom')
    r.hset(8000, 'job', 'SALESMAN')
    r.hmset(9000, {'ename': 'scott', 'job': 'SALESMAN', 'deptno': 10})
    print(r.hget(8000, 'ename'))
    print(r.hmget(8000, 'ename', 'job'))
    print(r.hgetall(8000))
    print(r.hkeys(8000))
    print(r.hlen(8000))
    print(r.hexists(8000, 'job'))
    print(r.hvals(8000))
    print(r.hdel(8000, 'job'))
    print(r.hincrby(9000, 'deptno', 10))
