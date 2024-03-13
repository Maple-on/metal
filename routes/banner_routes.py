import os
import uuid
from pathlib import Path
from random import randint

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from fastapi.responses import FileResponse

from services.banner_service.banner_model import CreateBannerModel
from services.banner_service.banner import create, get_by_id, get_list, delete
from database import database


router = APIRouter(
    prefix="/banners",
    tags=['Banners']
)

get_db = database.get_db

IMAGE_DIR = Path() / "images"


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_banner(request: CreateBannerModel = Depends(), picture: UploadFile = File(...), session: Session = Depends(get_db)):
    filename = f"{uuid.uuid4()}.jpg"
    banner_id = create(request, filename, session)
    data = await picture.read()
    save_to = IMAGE_DIR / filename
    print(IMAGE_DIR)
    with open(save_to, 'wb') as f:
        f.write(data)
    return {"file_name": filename, "banner_id": banner_id}


@router.get("/")
def get_banner(id: int, session: Session = Depends(get_db)):
    path = get_by_id(id, session)
    return FileResponse(path)


@router.delete("/")
def delete_banner(id: int, session: Session = Depends(get_db)):
    path = get_by_id(id, session)
    delete(id, session)
    os.unlink(path)