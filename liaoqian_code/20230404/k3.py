import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.flushall()
    r.sadd('employee', 8000, 8001, 8002)
    r.expireat('employee', 1712202900)
    r.persist('employee')
    print(r.type('employee'))