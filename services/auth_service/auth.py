import random

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from config import SmsSettings
import requests
import json

from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service.auth_model import Token
from database.models import User, Verification, Client
from database.hashing import Hash
from services.auth_service.token import create_access_token, create_access_token_for_guest, create_access_token_for_client
from services.auth_service.auth_model import VerificationRequestForLogin, VerificationRequestForSignUp
from services.client_service.client import create
from services.client_service.client_model import CreateClientModel

sms_settings = SmsSettings()


def c_log_in(request: OAuth2PasswordRequestForm, db: Session):
    client = db.query(Client).filter(Client.phone == request.username).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid phone number")

    access_token = create_access_token(data={"sub": request.username})
    token = Token(
        access_token=access_token,
        token_type="bearer"
    )
    return token


def log_in(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email address")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.username})
    token = Token(
        access_token=access_token,
        token_type="bearer"
    )
    return token


def get_sms_token():
    url = "https://notify.eskiz.uz/api/auth/login"

    payload = {'email': sms_settings.SMS_EMAIL, 'password': sms_settings.SMS_PWD}
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    parsed_data = json.loads(response.text)
    token = parsed_data['data']['token']
    return token


def refresh_sms_token():
    url = "https://notify.eskiz.uz/api/auth/refresh"

    payload = {}
    headers = {}

    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response


def send_sms_code(phone_number: str, db: Session):
    code = ''.join(str(random.randint(0, 9)) for _ in range(5))
    response = send_sms(phone_number, "Ваш код от Metally - " + code + " Никому его не сообщайте")
    parsed_data = json.loads(response.text)
    sms_id = parsed_data['id']
    create_verification(sms_id, code, db)
    return {"sms_id": sms_id}


def send_sms(phone_number: str, message: str):
    token = get_sms_token()
    url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    files = []

    payload = {
        'mobile_phone': phone_number,
        'message': message,
        'from': '4546'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response


def verify_sms_code_login(request: VerificationRequestForLogin, db: Session):
    verification = db.query(Verification).filter(Verification.id == request.sms_id).first()
    if not verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid SMS ID")

    if verification.code == request.code:
        client = db.query(Client).filter(Client.phone == request.phone_number).first()
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invalid phone number")
        else:
            access_token = create_access_token_for_client(data={"sub": request.phone_number})
            token = Token(
                access_token=access_token,
                token_type="bearer"
            )
            return {
                "client": client,
                "token": token
            }
    return False


def verify_sms_code_signup(request: VerificationRequestForSignUp, db: Session):
    verification = db.query(Verification).filter(Verification.id == request.sms_id).first()
    if not verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid SMS ID")

    if verification.code == request.code:
        client = db.query(Client).filter(Client.phone == request.phone_number).first()
        if not client:
            client = CreateClientModel(username=request.name, phone=request.phone_number)
            client = create(client, db)
        access_token = create_access_token_for_client(data={"sub": request.phone_number})
        token = Token(
            access_token=access_token,
            token_type="bearer"
        )
        return {
            "client": client,
            "token": token
        }
    return False


def create_verification(sms_id: str, code: str, db: Session):
    new_verification = Verification(
        id=sms_id,
        code=code
    )
    db.add(new_verification)
    db.commit()
    db.refresh(new_verification)
    db.close()

    return new_verification.id
