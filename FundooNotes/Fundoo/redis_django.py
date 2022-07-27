import redis
from django.conf import settings


class RedisService:
    redis_object = redis.Redis(**settings.REDIS_SETTINGS)

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
    def delete(cls, user_id):
        cls.redis_object.delete(cls, user_id)

    @classmethod
    def all_delete(cls):
        cls.redis_object.flushall()
