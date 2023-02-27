import os
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db
from flask import session, current_app
import functools
from flask import redirect, g, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort


class User:
    """User is an object contain all the information you need about a specific user,
    whether they were registering or loginning , User will help you encapsulate all seperate
    data and functoinality that relative to users.
    """

    def __init__(self, username, password, email=None, error=None) -> None:

        self.error = error
        self.username = username
        self.password = password
        # self.email = email

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

        if self.error is None:
            if not password:
                self.error = "Missing password!"

            if self.error is None:
                self._password = password

    # @property
    # def email(self):
    #     return self._email

    # @email.setter
    # def email(self, email):

    #     if not email:
    #         self.error = "Missing email"

    #     if not validators.email(email):
    #         self.error = "Invalide email"

    #     if self.error == None:
    #         self._email = email

    def register(self):
        """the register method allow you to register the user if and only if
        all the conditions have been satisfied, like username and password and a valid email,
        and it also handl exceptoins like if the username is already exist, and if so, it will assign
        the error atribute to an error message "Username is already exist!" for instance.
        """
        if self.error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (self.username, generate_password_hash(self.password)),
                )
                db.commit()
            except db.IntegrityError:
                self.error = f"Username {self.username} is already exist"

    def check(self):
        """_summary_
        check the existence of a user in the db,
        this method is used for the login view validate that the username is indeed
        in the db, and if so, it will check the matching password

        Returns:
            boolen: return True if the user was in the db and password matched,
            return False otherwise
        """
        if self.error is not None:
            return False

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (self.username,)
        ).fetchone()
        if user is None:
            self.error = f"{self.username} doesn't exist!"
            return False

        if check_password_hash(user["password"], self.password):
            self.user_id = user["id"]
            return True

        self.error = "Incorrect password"
        return False

    def login(self):
        """log the user in after checking there is no errors by clearing the session and assigning user_id to it"""
        if self.error is None:
            session.clear()
            session["user_id"] = self.user_id

    def __str__(self) -> str:
        return (
            f"username: {self.username}, password: {self.password}, error: {self.error}"
        )


def login_required(view):
    """_summary_
    the decorator don't let visitors enter a specific view unless they have loged in
    """

    @functools.wraps(view)
    def wrapper_login_required(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapper_login_required


def allowed_extention(filename):
    ALLOWED_EXTENTIONS = {"png", "jpeg", "jpg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS


def save_picture(file, id):
    db = get_db()
    picture_name = secure_filename(file.filename)
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], picture_name))
    
    try:
        db.execute(
            "INSERT INTO picture (owner_id, picture_name) VALUES (?,?)",
            (id, picture_name),
        )
        db.commit()
    except db.IntegrityError:
        return False

    return True


def get_designer(id=None):
    """fetch one or more designers from db based on id

    Args:
        id(integer)
    Returns:
        _type_: list or designers if id was None, one designer otherwise
        >> abort a 404 error if designer was not exist in db
    """
    db = get_db()

    if id is not None:
        designer = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
        if designer is None:
            abort(404)
    else:
        designer = db.execute("SELECT * FROM user").fetchall()

    return designer

def get_picture(id=None):
    
	db = get_db()

	if id is not None:
		picture = db.execute("SELECT * FROM picture where owner_id = ? ORDER BY published DESC",(id,)).fetchall()
	else:
		picture = db.execute("SELECT * FROM picture").fetchall()

	return picture



def check_designer(id):
    """return True if the designer that trying to save picture into db is the owner of that account,abort 401 error otherwise.
    """
    if id == g.user["id"]:
        return True

    abort(401)





def check_picture(id, user_id):
    # Check if the picture exist in db
    db = get_db()
    id = int(id)
    picture = db.execute("SELECT * FROM picture WHERE id = ?",
            id,).fetchone()
    if picture is not None:
        return True 

    return False


def delete_picture(id):
    try:
        get_db().execute("DELETE FROM picture WHERE id = ?", id)
    except:
        return "no way home so we couldn't delete the picture alone"     
