from datetime import datetime, timedelta
from jose import JWTError, jwt
from services.auth_service.auth_model import TokenData
from config import TokenSettings

token_settings = TokenSettings()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.secret_key, algorithm=token_settings.algorithm)
    return encoded_jwt


def create_access_token_for_client(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.secret_key_2, algorithm=token_settings.algorithm)
    return encoded_jwt


def create_access_token_for_guest(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_settings.guest_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.secret_key_2, algorithm=token_settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, token_settings.secret_key, algorithms=[token_settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception


def verify_client_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, token_settings.secret_key_2, algorithms=[token_settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
