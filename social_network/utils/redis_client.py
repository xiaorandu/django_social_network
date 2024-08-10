import redis
from django.conf import settings


#Manages the connection to the Redis server. It creates a single connection instance that can be reused across different operations.
class RedisClient:
    conn = None

    @classmethod
    def get_connection(cls):
     
        if cls.conn:
            return cls.conn
        cls.conn = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )
        return cls.conn

    @classmethod
    def clear(cls):

        if not settings.TESTING:
            raise Exception("You can not flush redis in production environment")
        conn = cls.get_connection()
        conn.flushdb()