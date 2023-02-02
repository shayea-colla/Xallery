from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db
from flask import session
import validators


class User():
    def __init__(self, username, password,email=None, error=None) -> None:

        self.error = error
        self.username = username
        self.password = password
        self.email = email
        self._email= email

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):

        if not username:
            self.error = "Missing username!"

        if self.error is None:
            self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):

        if not password:
            self.error = "Missing password!"

        if self.error is None:
            self._password = password

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        
        if not email:
            self.error = "Missing email"
        
        if not validators.email(email):
            self.error = "Invalide email"
        
        if self.error == None:
            self._email = email

    def register(self):
        if self.error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password,email) VALUES (?,?,?)",
                    (self.username, generate_password_hash(self.password), self.email),
                )
                db.commit()
            except db.IntegrityError:
                self.error = f"Username {self.username} is already exist"

    def check(self):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (self.username,)
        ).fetchone()
        if user is not None:
            if check_password_hash(user["password"], self.password):
                self.user_id = user['id']
                return True
            return False

        return False

    def login(self):
        if self.error is None:
            session.clear()
            session['user_id'] = self.user_id
            
    def __str__(self) -> str:
        return f'username: {self.username}, password: {self.password}, error: {self.error}, email: {self._email}'
