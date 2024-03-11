from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.client_service.client_model import CreateClientModel, UpdateClientModel
from database.models import Client
from datetime import datetime


def create(request: CreateClientModel, db: Session):
    new_client = Client(
        username=request.username,
        phone=request.phone,
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client


def get_list(db: Session):
    client = db.query(Client).all()

    return client


def get_by_id(id: int, db: Session):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Client with id {id} not found")

    return client


def update(id: int, request: UpdateClientModel, db: Session):
    client = db.get(Client, id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Client with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(client, key, value)
    setattr(client, "updated_at", datetime.now())
    db.commit()
    db.refresh(client)

    return client


def delete(id: int, db: Session):
    client = db.query(Client).filter(Client.id == id)
    if not client.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Client with id {id} not found")

    client.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


def get_client(id: int, db: Session):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Client with id {id} not found")

    return client.phone
