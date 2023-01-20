from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from socnet.etc.readyaml import read_config_yaml
from socnet.models.auth_models import TokenData, User, UserInDB
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from socnet.DB_manipulations.db_session import session_init
from socnet.DB_manipulations.db_methods import UserRepository


ALGIRITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = read_config_yaml()['secret_key']

SESSION = session_init()
USERMANIPULATOR = UserRepository(SESSION)


def get_list_of_users(to_parse):
    list_of_users = {}
    for user in to_parse:
        user_to_add = {}
        user_to_add['id'] = str(user.id)
        user_to_add['username'] = str(user.username)
        user_to_add['hashedpassword'] = str(user.hashedpassword)
        list_of_users[str(user.username)] = user_to_add

    return list_of_users


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        user_dict = {
            'hashed_password': user_dict['hashedpassword'],
            'username': user_dict['username'],
            'id': user_dict['id']
        }
        return UserInDB(**user_dict)


def authenticate_user(db_of_users, username: str, password: str):
    user = get_user(db_of_users, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def check_user(db_of_users, username: str, password: str):
    user = get_user(db_of_users, username)
    if not user:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGIRITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate:': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGIRITHM])
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(
        get_list_of_users(USERMANIPULATOR.get_list()),
        username=token_data.username)

    if user is None:
        raise credentials_exception
    return user
