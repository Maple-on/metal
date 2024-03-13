from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.metal_service.metal_model import CreateMetalModel, UpdateMetalModel, MetalModel
from database.models import Metal
from datetime import datetime
from sqlalchemy import desc, asc


def create(request: CreateMetalModel, db: Session):
    new_metal = Metal(
        category=request.category,
        subcategory=request.subcategory,
        price=request.price,
    )
    db.add(new_metal)
    db.commit()
    db.refresh(new_metal)

    return new_metal


def get_list(db: Session):
    metals = db.query(Metal).order_by(asc(Metal.category)).order_by(asc(Metal.id)).all()

    total_count = len(metals)
    metal_list = []

    for metal in metals:
        each_metal = MetalModel(
            id=metal.id,
            category=metal.category,
            subcategory=metal.subcategory,
            price=metal.price,
            available=metal.available,
            created_at=metal.created_at,
            updated_at=metal.updated_at
        )
        metal_list.append(each_metal)

    db.close()
    return {
        "metals": metal_list,
        "total_count": total_count
    }


def get_by_id(id: int, db: Session):
    metal = db.query(Metal).filter(Metal.id == id).first()
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal with id {id} not found")

    specific_metal = MetalModel(
        id=metal.id,
        category=metal.category,
        subcategory=metal.subcategory,
        price=metal.price,
        available=metal.available,
        created_at=metal.created_at,
        updated_at=metal.updated_at
    )

    return specific_metal


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

    return metal


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


def get_metal(category: str, subcategory: str, db: Session):
    metal = db.query(Metal).filter(Metal.category == category, Metal.subcategory == subcategory).first()
    if not metal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Metal not found")
    db.close()
    return {
        "id": metal.id,
        "category": metal.category,
        "subcategory": metal.subcategory,
        "price": metal.price,
        "available": metal.available
    }


