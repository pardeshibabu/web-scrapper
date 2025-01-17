import redis

class Cache:
    def __init__(self, redis_url="redis://localhost"):
        self.redis = redis.StrictRedis.from_url(redis_url)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        self.redis.set(key, value)
