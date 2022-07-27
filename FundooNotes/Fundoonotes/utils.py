import json

from Fundoo.redis_django import RedisService


class NoteRedis:
    @classmethod
    def _save(cls, user_id: str, note_dict: dict):
        RedisService.set(str(user_id), json.dumps(note_dict))

    @classmethod
    def extract(cls, user_id):
        user_id = str(user_id)
        if not RedisService.get(user_id):
            return {}
        return json.loads(RedisService.get(user_id))

    @classmethod
    def update(cls, user_id: str, note_dict: dict):
        """
        saving Note data into redis
        key = user_id
        value = {note_1:{'id':1,'title':'note title',...},note_2:{'id':2,'title':'note title',...}}
        """
        existing_data = cls.extract(user_id)
        existing_data.update({note_dict['id']: note_dict})
        cls._save(user_id=user_id, note_dict=existing_data)

