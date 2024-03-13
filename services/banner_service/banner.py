from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from config import BannerSettings
from services.banner_service.banner_model import CreateBannerModel, BannerModel
from database.models import Banner
from fastapi import HTTPException, status, UploadFile, File

banner_settings = BannerSettings()


def create(request: CreateBannerModel, filename: str, db: Session):
    new_banner = Banner(
        image_url="images/"+filename,
        desc=request.name
    )
    db.add(new_banner)
    db.commit()
    db.refresh(new_banner)
    db.close()

    return new_banner.id


def get_list(db: Session):
    banners = db.query(Banner).all()
    banner_list = []

    for banner in banners:
        each_banner = BannerModel(
            id=banner.id,
            image_url=banner_settings.BASE_URL+str(banner.id),
            desc=banner.desc,
            created_at=banner.created_at
        )
        banner_list.append(each_banner)

    db.close()
    return {"banners": banner_list}


def get_by_id(id: int, db: Session):
    banner = db.query(Banner).filter(Banner.id == id).first()
    if not banner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Client with id {id} not found")

    return banner.image_url


def delete(id: int, db: Session):
    banner = db.query(Banner).filter(Banner.id == id)
    if not banner.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Banner with id {id} not found")

    banner.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT