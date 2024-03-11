from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.metal_service.metal_model import CreateMetalModel, UpdateMetalModel
from database.models import Metal
from datetime import datetime


def create(request: CreateMetalModel, db: Session):
    new_metal = Metal(
        type=request.type,
        name=request.name,
        price=request.price,
    )
    db.add(new_metal)
    db.commit()
    db.refresh(new_metal)

    return new_metal


def get_list(db: Session):
    user = db.query(Metal).all()

    return user


def get_by_id(id: int, db: Session):
    metal = db.query(Metal).filter(Metal.id == id).first()
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")

    return metal


def update(id: int, request: UpdateMetalModel, db: Session):
    metal = db.get(Metal, id)
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(metal, key, value)
    setattr(metal, "updated_at", datetime.now())
    db.commit()
    db.refresh(metal)

    return user


def delete(id: int, db: Session):
    metal = db.query(Metal).filter(Metal.id == id)
    if not metal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")

    metal.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


def check_if_metal_is_available(id: int, db: Session):
    metal = db.get(Metal, id)
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")
    return metal.available


def get_metal(id: int, db: Session):
    metal = db.query(Metal).filter(Metal.id == id).first()
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")

    return {
        "type": metal.type,
        "name": metal.name,
        "price": metal.price,
        "available": metal.available
    }

