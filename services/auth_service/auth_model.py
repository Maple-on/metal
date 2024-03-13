from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Method(str, Enum):
    login = "Login"
    sign_up = "Sign_up"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class VerificationRequest(BaseModel):
    sms_id: str
    code: str
    phone_number: str
    method: Method
