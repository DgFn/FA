import jwt
from fastapi import APIRouter, HTTPException, Depends, Request
from repositories.auth import JWTBearer
from api.schemas.users import CreateUserSchema, UserSchema, UpdateUserSchema, AuthSchema
from database.engine import Session
from database.models import User, Log_Auth
from repositories import users as user_repo
from repositories.users import create_jwt_token

router = APIRouter()


@router.post('/users', response_model=CreateUserSchema)
def create_user(user_data: CreateUserSchema):
    hash_password = user_repo.hash_password(user_data.password)
    user = User(login=user_data.login, password=hash_password)

    with Session() as session:
        session.add(user)
        session.commit()

    return user


@router.post('/users/auth')
def auth_user(user_data: AuthSchema):
    with Session() as session:
        user = user_repo.get_login(session, user_data.login)
        if user is None:
            raise HTTPException(status_code=400, detail='Invalid login or password')

        is_password_correct = user_repo.verify_password(user_data.password, user.password)
        if not is_password_correct:
            raise HTTPException(status_code=400, detail='Invalid login or password')

        auth_user = Log_Auth(user_id=user.id)
        session.add(auth_user)
        session.commit()
        jwt_token = create_jwt_token({'sub': user.id, 'log_sub': auth_user.id})
    return {'token': jwt_token}


@router.post('/logout', dependencies=[Depends((JWTBearer()))])
def logout_user(request: Request):
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = user_repo.data_token(token)

    with Session() as session:
        log_entry = user_repo.get_log_current(session, decoded_data['user_id'], decoded_data['log_id'])
        if log_entry:
            session.delete(log_entry)
            session.commit()
            return {'message': 'Successfully logged out'}
        raise HTTPException(status_code=401, detail="Invalid token.")
@router.get('/sessions', dependencies=[Depends((JWTBearer()))])
def active_session(request: Request):
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = user_repo.data_token(token)
    with Session() as session:
        log_entry = user_repo.get_log_current(session, decoded_data['user_id'], decoded_data['log_id'])
        if log_entry:
            logs = user_repo.get_log_all(session, decoded_data['user_id'])
            return logs
        raise HTTPException(status_code=401, detail="Invalid token.")

@router.post('/delete_sessions', dependencies=[Depends((JWTBearer()))])
def delete_session(request: Request):
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = user_repo.data_token(token)
    with Session() as session:
        log_entry = user_repo.get_log_current(session, decoded_data['user_id'], decoded_data['log_id'])
        if log_entry:
            delete_sessions = user_repo.get_logs_excluding_specific(
                session,
                decoded_data['user_id'],
                decoded_data['log_id']
            )
            for delete_session in delete_sessions:
                session.delete(delete_session)
                session.commit()
            return {'message': 'Successfully deleted sessions'}
        raise HTTPException(status_code=401, detail="Invalid token.")



@router.get('/users', dependencies=[Depends((JWTBearer()))], response_model=list[UserSchema])
def get_users(request: Request):

    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data= user_repo.data_token(token)
    with Session() as session:
        log_entry = user_repo.get_log_current(session, decoded_data['user_id'], decoded_data['log_id'])
        if log_entry:
            users = user_repo.get_users(session)
            return users
        raise HTTPException(status_code=401, detail="Invalid token.")


@router.get('/users/{user_id}')
def get_user(user_id: int):
    with Session() as session:
        user = user_repo.get_user(session, user_id=user_id)
    return user


@router.patch('/users/{user_id}', response_model=UpdateUserSchema)
def update_user(user_id: int, new_user_data: UpdateUserSchema):
    with Session() as session:
        user = user_repo.get_user(session, user_id=user_id)
        user.login = new_user_data.login
        session.commit()

    return user
