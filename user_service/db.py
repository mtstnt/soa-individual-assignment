from nameko.dependency_providers import DependencyProvider
import sqlite3

class UserDB:
	def __init__(self, conn: sqlite3.Connection):
		self.conn = conn

	def find_user(self, username: str) -> any:
		cursor = self.conn.cursor()
		results = cursor.execute("SELECT * FROM users WHERE username = ?", [username])

		if results.rowcount == 0:
			cursor.close()
			return None

		return results.fetchone()

	def get_user_count(self, username: str) -> int:
		cursor = self.conn.cursor()
		result = cursor.execute("SELECT * FROM users WHERE username = ?", [username])
		return result.rowcount

	def insert_user(self, username: str, password: str) -> bool:
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, password])
		self.conn.commit()
		return True

class Database(DependencyProvider):
	def setup(self):
		self.connection = sqlite3.connect("user_db.db")
		self.connection.row_factory = sqlite3.Row
		cursor = self.connection.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS users ( 
				id INTEGER PRIMARY KEY, 
				username VARCHAR(255) UNIQUE NOT NULL,
				password VARCHAR(255) NOT NULL
			)
		""")
		
	def get_dependency(self, worker_ctx):
		return UserDB(self.connection)