from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import database
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service.auth import c_log_in, log_in, send_sms_code, verify_sms_code_login, verify_sms_code_signup
from services.auth_service.auth_model import VerificationRequestForLogin, VerificationRequestForSignUp

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    return log_in(request, session)


# @router.post('/clogin')
# def clogin(request: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
#     return c_log_in(request, session)


@router.post("/send_code")
def send_code(number: str, session: Session = Depends(get_db)):
    return send_sms_code(number, session)


@router.post("/verify_login")
def verify_code(request: VerificationRequestForLogin, session: Session = Depends(get_db)):
    return verify_sms_code_login(request, session)


@router.post("/verify_singup")
def verify_code(request: VerificationRequestForSignUp, session: Session = Depends(get_db)):
    return verify_sms_code_signup(request, session)
