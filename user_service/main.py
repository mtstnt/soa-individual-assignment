from datetime import timedelta
from nameko.rpc import rpc

import bcrypt
import secrets
import db

class UserService:
    name = "user_service"

    userdb = db.Database()

    @rpc
    def login(self, username, password) -> dict: 
        row = self.userdb.find_user(username)
        print(f"{row['id']} {row['username']} {row['password']}")
        if not row:
            return { "error": 1, "message": "User not found!" }

        row_passwd = row['password']
        if not bcrypt.checkpw(password.encode(), row_passwd):
            return { "error": 1, "message": "Invalid credentials!" }
        
        token = secrets.token_urlsafe(16)
        return { "error": 0, "message": "Successfully logged in", "user_id": row['id'], "token": token }

    @rpc
    def register(self, username: str, password: str):
        user_count = self.userdb.get_user_count(username)

        if user_count > 0:
            return { "error": 1, "message": f"User with username {username} already exists" }

        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode(), salt)
        if not self.userdb.insert_user(username, hashed_pw):
            return { "error": 1, "message": "Failed to insert user" }
            
        token = secrets.token_urlsafe(16)
        return { "error": 0, "message": f"Successfully registered user {username}", "token": token }