from nameko.dependency_providers import DependencyProvider
import redis

class Redis:
	def __init__(self, conn: redis.Redis):
		self.conn = conn

	def set(self, key: str, value: any):
		self.conn.set(key, value)

	def get(self, key: str) -> any:
		return self.conn.get(key)

class RedisApi(DependencyProvider):
	def setup(self):
		self.connection = redis.Redis(host="localhost", port=6379, db=0)
		
	def get_dependency(self, worker_ctx):
		return Redis(self.connection)