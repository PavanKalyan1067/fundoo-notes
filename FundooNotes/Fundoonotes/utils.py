import json

from Fundoo.redis_django import RedisService


class NoteRedis:
    @classmethod
    def save(cls, value, key):
        RedisService.set(key, json.dumps(value))

    @classmethod
    def extract(cls, key):
        if not RedisService.get(key):
            return {}
        return json.loads(RedisService.get(key))

    @classmethod
    def update(cls, key, value):
        existing_data = cls.extract(key)
        existing_data.update({key: value})
        cls.save(key=key, value=existing_data)
