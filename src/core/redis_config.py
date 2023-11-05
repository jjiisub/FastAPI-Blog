import redis

from src.utils.config import Settings


def get_redis():
    '''
    Redis 연결 관리 함수
    '''
    rd = redis.Redis(host=Settings().REDIS_HOST, port=Settings().REDIS_PORT, db=Settings().REDIS_DATABASE)
    if rd: return rd
    else: raise Exception("Redis가 연결되지 않았습니다.")
