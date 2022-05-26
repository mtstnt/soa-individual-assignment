from datetime import timedelta
from nameko.rpc import rpc
import redis
import bcrypt
import secrets
import pickle

class UserService:
    name = "user_service"

    redis_client: redis.Redis

    def __init__(self) -> None:
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)

    @rpc
    def login(self, username, password) -> dict: 
        passwd = self.redis_client.get(f"USER:{username}")
        if passwd is None:
            return { "error": 1, "message": "Invalid credentials" }
        
        if not bcrypt.checkpw(password, passwd):
            return { "error": 1, "message": "Invalid credentials" }

        # Correct login info
        token = secrets.token_urlsafe(16)
        self.redis_client.set(f"SESS:{token}", username, ex=3 * timedelta.seconds)
        return { "error": 0, "message": "Successfully logged in" }

    @rpc
    def register(self, username, password):
        user_count = self.redis_client.exists(f"USER:{username}")

        if user_count == 0:
            salt = bcrypt.gensalt()
            self.redis_client.set(f"USER:{username}", bcrypt.hashpw(password, salt))
            return { "error": 0, "message": f"Successfully registered user {username}" }

        return { "error": 1, "message": f"User with username {username} already exists" }