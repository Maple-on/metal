from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, asc, desc
from decimal import Decimal
from datetime import datetime

from services.auth_service.auth import send_sms
from services.metal_service.metal import get_metal
from services.client_service.client import get_client
from services.order_service.order_model import CreateOrder, CreateBaseOrder, UpdateOrder, OrderModel
from database.models import Order, Client, Metal


def create(request: CreateBaseOrder, db: Session):
    metal = get_metal(request.metal_category, request.metal_subcategory, db)
    client_phone = get_client(request.client_id, db)
    new_order = Order(
        client_id=request.client_id,
        metal_id=metal['id'],
        amount=request.amount,
        metal_price=metal['price']
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()

    total = request.amount * Decimal(metal['price'])
    if metal['available']:
        status = "Есть в наличии"
    else:
        status = "Нет в наличии"
    message = f"Метал {metal['category']} {metal['subcategory']} - {status} \nОбщая стоимость: {metal['price']} * {request.amount} = {total}"
    send_sms(client_phone, message)
    return new_order


def get_list(offset: int, limit: int, db: Session):
    orders = db.query(Order, Client.username, Client.phone, Metal.category, Metal.subcategory).join(Client, Order.client_id == Client.id).join(Metal, Order.metal_id == Metal.id)
    orders = orders.offset(offset).limit(limit).all()

    order_list = []

    for order, username, phone_number, category, subcategory in orders:
        each_order = OrderModel(
            id=order.id,
            client_name=username,
            client_phone=phone_number,
            order={
                "metal_category": category,
                "metal_subcategory": subcategory,
                "metal_price": order.metal_price,
                "amount": order.amount,
                "unit": order.unit
            },
            total_sum=order.metal_price*order.amount,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
        order_list.append(each_order)

    db.close()
    return order_list


def get_by_id(id: int, db: Session):
    orders = (db.query(Order, Client.username, Client.phone, Metal.category, Metal.subcategory)
            .join(Client, Order.client_id == Client.id)
            .join(Metal, Order.metal_id == Metal.id)).first()
    order, username, phone_number, category, subcategory = orders[0], orders[1], orders[2], orders[3], orders[4]

    specific_order = OrderModel(
        id=order.id,
        client_name=username,
        client_phone=phone_number,
        order={
            "metal_category": category,
            "metal_subcategory": subcategory,
            "metal_price": order.metal_price,
            "amount": order.amount,
            "unit": order.unit
        },
        total_sum=order.metal_price * order.amount,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at
        )

    db.close()
    return specific_order


def delete(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")

    order.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


def update(id: int, request: UpdateOrder, db: Session):
    order = db.get(Order, id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    setattr(order, "updated_at", datetime.now())
    db.commit()
    db.refresh(order)

    return order
