from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.auth_service.token import verify_token, verify_client_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_for_client = OAuth2PasswordBearer(tokenUrl="c_login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)


def get_current_client(data: str = Depends(oauth2_scheme_for_client)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_client_token(data, credentials_exception)
