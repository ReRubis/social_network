from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from socnet.DB_manipulations.db import User as UserDB
from socnet.DB_manipulations.db_methods import UserRepository
from socnet.DB_manipulations.db_session import session_init
from socnet.depend import authdepen
from socnet.etc.readyaml import read_config_yaml
from socnet.models.auth_models import User

ALGIRITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = read_config_yaml()['secret_key']


def build_user_repository(session=Depends(session_init)):
    return UserRepository(session)


router = APIRouter(
    prefix='/users',
    tags=['authentification'],
)


@router.post('/register')
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(build_user_repository)
):
    """Register the user with passed down login and password"""

    list_of_users = {}
    user: User

    for user in repo.get_list():
        user_to_add = {}
        user_to_add['id'] = str(user.id)
        user_to_add['username'] = str(user.username)
        user_to_add['hashedpassword'] = str(user.hashedpassword)
        list_of_users[str(user.username)] = user_to_add

    user = authdepen.check_user(
        list_of_users,
        form_data.username,
        form_data.password)

    if not user:
        repo.save(
            UserDB(
                username=form_data.username,
                hashedpassword=authdepen.get_password_hash(form_data.password)),
        )
        return {'Message': 'Done'}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with that login already exists",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(build_user_repository)
):
    """Returns JWT token when passed login and password"""
    list_of_users = {}

    user: User
    for user in repo.get_list():
        user_to_add = {}
        user_to_add['id'] = str(user.id)
        user_to_add['username'] = str(user.username)
        user_to_add['hashedpassword'] = str(user.hashedpassword)
        list_of_users[str(user.username)] = user_to_add

    user = authdepen.authenticate_user(
        list_of_users,
        form_data.username,
        form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authdepen.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/who_am_i', response_model=User)
async def get_user(
        current_user: User = Depends(authdepen.get_current_user)):
    """Returns current user"""
    return current_user
