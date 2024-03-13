from pydantic import BaseModel
from fastapi import UploadFile


class CreateBannerModel(BaseModel):
    name: str


class BannerModel(BaseModel):
    name: str
    image_url: str