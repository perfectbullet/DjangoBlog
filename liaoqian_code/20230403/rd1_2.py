import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    keydict = {}
    keydict['username'] = 'jack'
    keydict['age'] = 24
    keydict['sex'] = 'male'
    print(r.mset(keydict))
    list = ['username', 'age', 'sex']
    print(r.mget(list))

    r.setex('temp', 60, 'ABCD')
    print(r.get('temp'))
    print(r.append('temp', '1234'))
    print(r.get('temp'))

    r.setex('num', 100, 0)
    print(r.incr('num'))
    print(r.get('num'))
    print(r.incrby('num', 35))
    print(r.incrby('num', -1))
    print(r.incrbyfloat('num', 0.5))

    r.setex('nu', 200, 10)
    print(r.decr('nu'))
    print(r.decrby('nu', 5))
