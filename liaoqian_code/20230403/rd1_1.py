import redis

if __name__ == '__main__':
    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.set('email', 'scott@163.com')

    print(r.getrange('email', 0, 3))
    print(r.strlen('email'))

    r.setex('username', 5, 'scott')
    print(r.get('username'))
