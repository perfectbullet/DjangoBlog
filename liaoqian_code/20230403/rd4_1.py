import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.flushall()
    r.sadd('empno', 8000, 8001, 8002, 9000)
    print(r.smembers('empno'))
    print(r.scard('empno'))
    print(r.sismember('empno', 8000))
    print(r.srem('empno', 8000))
    # print(r.delete('empno'))
    print(r.spop('empno'))
    print(r.srandmember('empno', 2))
