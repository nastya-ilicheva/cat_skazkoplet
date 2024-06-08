import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
import base64
import uuid


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'{self.login}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Story(SqlAlchemyBase, UserMixin):
    __tablename__ = 'story'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enable = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)

    # user = relationship("User", backref="login", foreign_keys=[user_id])

    def __repr__(self):
        return f'{self.id}: {self.title}'


class Message(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    story_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("story.id"))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'{self.id}: {self.story_id} - {self.text}'


class Full_Stories(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Full_Stories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    story_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
