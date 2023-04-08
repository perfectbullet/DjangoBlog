import redis
try:
    pool = redis.ConnectionPool(
        host='49.232.208.236',
        port=6378,
        db=0,
        max_connections=20
    )
except Exception as e:
    print(e)

