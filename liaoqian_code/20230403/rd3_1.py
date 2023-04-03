import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.flushdb()
    r.rpush('dname', '技术部', '后勤部', '售后部')
    r.lpush('dname', '秘书处')
    r.lset('dname', 2, '销售部')
    print(r.lrange('dname', 0, -1))
    print(r.llen('dname'))
    print(r.lindex('dname', 0))
    print(r.linsert('dname', 'before', '秘书处', '董事会'))
    print(r.lpop('dname'))
    print(r.rpop('dname'))
    