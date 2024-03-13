from datetime import datetime
from pydantic import BaseModel


class CreateBannerModel(BaseModel):
    name: str


class BannerModel(BaseModel):
    id: int
    image_url: str
    desc: str
    created_at: datetime
