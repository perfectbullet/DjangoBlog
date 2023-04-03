import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.zadd('keyword', {'李彦宏': 1000})
    print(r.zrem('keyword', '李彦宏'))
    print(r.zremrangebyrank('keyword', 0, 2))
    r.zadd('keyword', {'张朝阳': 2200, '鹿晗': 3600, '马云': 5000})
    print(r.zremrangebyrank('keyword', 0, -3))
    print(r.zrange('keyword', 0, -1))
    print(r.zremrangebyscore('keyword', '-inf', '(5000'))
    print(r.zrange('keyword', 0, -1))