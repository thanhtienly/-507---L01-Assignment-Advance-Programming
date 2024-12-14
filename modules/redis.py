import redis

class RedisService:
    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, decode_responses=True)
        pass

    def set(self, key, value):
        self.r.set(key, value)

    def get(self, key):
        return self.r.get(key)