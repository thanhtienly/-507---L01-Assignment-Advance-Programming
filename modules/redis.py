import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RedisService:
    def __init__(self):
        self.r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), decode_responses=True)
        self.load_index()

        pass

    def load_index(self):
        index_file_path = os.environ.get("INDEX_FILE_PATH")
        with open(index_file_path, 'r') as file:
            data = json.load(file)
    
        self.r.set("index", json.dumps(data))
        
    def set(self, key, value):
        self.r.set(key, value)

    def get(self, key):
        return self.r.get(key)