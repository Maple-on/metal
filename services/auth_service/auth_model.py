from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class VerificationRequest(BaseModel):
    sms_id: str
    code: str
    phone: str
