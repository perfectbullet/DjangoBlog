import redis

if __name__ == '__main__':

    r = redis.Redis(host='49.232.208.236', port=6378, db=0)
    r.set('foo', 'bar')

    print(r.get('foo'))
