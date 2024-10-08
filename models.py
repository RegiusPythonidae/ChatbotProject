from extensions import db, login_manager

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password = db.Column(db.String)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String)
    country = db.Column(db.String)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    messages = db.relationship("Message")
    courses = db.relationship("Course", secondary="user_course")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Message(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    sent_time = db.Column(db.DateTime)
    is_chatbot = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
