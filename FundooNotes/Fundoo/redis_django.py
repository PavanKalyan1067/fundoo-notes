import redis

redis_data = {'db': 0, 'host': "localhost", 'port': 6379}


class RedisService:
    redis_object = redis.Redis(**redis_data)

    @classmethod
    def set(cls, user_id, data):

        cls.redis_object.set(user_id, data)

    @classmethod
    def get(cls, user_id):
        try:
            return cls.redis_object.get(user_id)
        except Exception as e:
            raise e

    @classmethod
    def Del(cls, user_id):

        cls.redis_object.delete(cls, user_id)

    @classmethod
    def All_Delete(cls):
        cls.redis_object.flushall()
