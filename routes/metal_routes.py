from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.metal_service.metal_model import CreateMetalModel, UpdateMetalShortModel
from services.metal_service.metal import create, get_by_id, delete, get_list, update
from database import database
from database.oauth2 import get_current_user
from services.user_service.user_model import UserModel

router = APIRouter(
    prefix="/metals",
    tags=['Metals']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def Create(request: CreateMetalModel, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return create(request, session)


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(session: Session = Depends(get_db)):
    return get_list(session)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def Get_by_id(id: int, session: Session = Depends(get_db)):
    return get_by_id(id, session)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def Update(id: int, request: UpdateMetalShortModel, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return update(id, request, session)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete(id: int, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return delete(id, session)
