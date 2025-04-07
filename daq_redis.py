# import redis 

class DAQRedis:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=decode_responses)
        
    def set_value(self, key, value):
        self.redis_client.set(key, value)
        
    def get_value(self, key):
        return self.redis_client.get(key)
