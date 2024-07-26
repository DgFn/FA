import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(32), unique=True, nullable=False)
    created = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    password = sa.Column(sa.String(length=255), nullable=False)

    log_auth = relationship('Log_Auth', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.login


class Log_Auth(Base):
    __tablename__ = 'log_auth'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
    created = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    user = relationship('User', back_populates='log_auth')
