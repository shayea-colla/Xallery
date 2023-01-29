from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from flask import session


class Validate:
    def __init__(self, username, password, view, error=None) -> None:

        self.username = username
        self.password = password
        self.error = error

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

    def register(self):
        if self.error is None:
            db = get_db()
            db.execute(
                "INSERT INTO user (username, password) VALUES (?,?)",
                (self.username, generate_password_hash(self.password)),
            )

    def validate_user(self):
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
