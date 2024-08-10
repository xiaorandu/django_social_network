from django.conf import settings

from utils.redis_client import RedisClient
from utils.redis_serializers import DjangoModelSerializer

# Provides utility methods to handle caching operations in Redis, such as loading objects into the cache and pushing new objects onto the cache.
class RedisHelper:
    #Serializes a list of Django model objects and stores them in Redis as a list.
    @classmethod
    def _load_objects_to_cache(cls, key, objects):

        conn = RedisClient.get_connection()

        serialized_list = []
        for obj in objects: 
            serialized_data = DjangoModelSerializer.serialize(obj) 
            serialized_list.append(serialized_data)

        if serialized_list: 
            conn.rpush(key, *serialized_list)  
            conn.expire(key, settings.REDIS_KEY_EXPIRE_TIME)  

    #check if the object in redis
    @classmethod
    def load_objects(cls, key, queryset):
        conn = RedisClient.get_connection()

        if conn.exists(key):
            serialized_list = conn.lrange(key, 0, -1)
            objects = []
            for serialized_data in serialized_list:
                deserialized_obj = DjangoModelSerializer.deserialize(serialized_data)
                objects.append(deserialized_obj)
            return objects
        
        # cache miss
        cls._load_objects_to_cache(key, queryset)

        return list(queryset)

    @classmethod
    def push_object(cls, key, obj, queryset):
        conn = RedisClient.get_connection()
        if not conn.exists(key):
    
            cls._load_objects_to_cache(key, queryset)
            return
        serialized_data = DjangoModelSerializer.serialize(obj)
        conn.lpush(key, serialized_data)  