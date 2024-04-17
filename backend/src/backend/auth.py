from backend.userdb import UserDBs
from datetime import datetime, timedelta
import jwt
import hashlib
import uuid

SECRET_KEY = "This is a secret key"
ALGORITHM = "HS256"

class AuthStore:
    def __init__(self, user_dbs):
        self.users = {}  # This stores username to password hash mappings
        self.temp_users = {}  # This stores temporary users
        self.user_dbs = user_dbs

    def register_user(self, username: str, password_hash: str):
        if username in self.users:
            return False  # User already exists
        self.users[username] = password_hash
        return True

    def validate_user(self, username: str, password_hash: str):
        if username in self.users and self.users[username] == password_hash:
            return True
        if username in self.temp_users and self.temp_users[username] == password_hash:
            return True
        return False

    def get_user_db(self, username: str):
        return self.user_dbs.get_user_db(username)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_temp_user(self):

        temp_username = str(uuid.uuid4())
        temp_password = str(uuid.uuid4())
        self.temp_users[temp_username] = temp_password
        return temp_username, temp_password
