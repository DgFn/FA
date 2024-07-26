import base64
import os
from datetime import timedelta, datetime, UTC

import sqlalchemy as sa
from sqlalchemy.orm import Session
from database.models import User, Log_Auth
import bcrypt
import jwt

SECRET_KEY = 'SSS'
ALGORITHM = 'HS256'
EXPIRATION_TIME = timedelta(hours=1)


def create_jwt_token(data: dict):
    expiration_time = datetime.now(tz=UTC) + EXPIRATION_TIME
    data.update({'exp': expiration_time.timestamp()})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data if decoded_data['exp'] >= datetime.now(tz=UTC).timestamp() else None

    except jwt.PyJWTError:
        return None


def data_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_data['sub']
        log_id = decoded_data['log_sub']
        return {'user_id': user_id, 'log_id': log_id}
    except jwt.PyJWTError:
        return None

def get_users(session: Session) -> list[User]:
    return list(session.execute(sa.select(User).order_by(User.id).limit(10)).scalars().all())

def get_user(session: Session, user_id: int) -> User | None:
    return session.scalar(sa.select(User).where(User.id == user_id))  # noqa

def get_log_current(session: Session, user_id: int, log_id: int) -> Log_Auth | None:
    return session.execute(sa.select(Log_Auth).where(
        Log_Auth.user_id == user_id,Log_Auth.id == log_id)
    ).scalar()
def get_logs_excluding_specific(session: Session, user_id: int, log_id_to_exclude: int):
    return session.execute(
        sa.select(Log_Auth).where(
            Log_Auth.user_id == user_id,
            Log_Auth.id != log_id_to_exclude
        )
    ).scalars().all()
def get_log_all(session: Session, user_id: int) -> list[Log_Auth]:
    return list(session.execute(sa.select(Log_Auth).order_by(Log_Auth.id).limit(10)).scalars())

def get_login(session: Session, user_login: str) -> User | None:
    return session.scalar(sa.select(User).where(User.login == user_login))  # noqa

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = base64.b64encode(hashed).decode('utf-8')
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed_password = base64.b64decode(hashed_password)
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
