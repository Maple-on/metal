from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class VerificationRequestForLogin(BaseModel):
    sms_id: str
    code: str
    phone_number: str


class VerificationRequestForSignUp(BaseModel):
    sms_id: str
    code: str
    phone_number: str
    name: str
