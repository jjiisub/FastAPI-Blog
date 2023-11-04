import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DATABASE = 0

def get_redis():

    rd = redis.Redis(host='localhost', port=6379, db=0)
    if rd: return rd
    else: raise Exception("Redis가 연결되지 않았습니다.")
