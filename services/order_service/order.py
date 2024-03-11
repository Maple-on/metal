from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text, asc, desc

from services.auth_service.auth import send_sms
from services.metal_service.metal import get_metal
from services.client_service.client import get_client
from services.order_service.order_model import CreateOrder, CreateBaseOrder, UpdateOrder
from database.models import Order


def create(request: CreateBaseOrder, db: Session):
    metal = get_metal(request.metal_id, db)
    client_phone = get_client(request.client_id, db)
    new_order = Order(
        client_id=request.client_id,
        metal_id=request.metal_id,
        amount=request.amount,
        metal_price=metal['price']
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total = request.amount * Decimal(metal['price'])
    if metal['available']:
        status = "Есть в наличии"
    else:
        status = "Нет в наличии"
    message = f"Метал {metal['type']} {metal['name']} - {status} \nОбщая стоимость: {metal['price']} * {request.amount} = {total}"
    print(message)
    send_sms(client_phone, message)
    return new_order


def get_list(offset: int, limit: int, db: Session):
    return True
    orders = db.query(OrderDetails, Client.name, Client.phone, PaymentDetails.payment_status, PaymentDetails.payment_method)\
        .join(Client, OrderDetails.client_id == Client.id)\
        .order_by(desc(OrderDetails.id))
    #
    # total_count = len(orders.all())
    # new_order_count = 0
    # new_order_sum = 0
    # completed_order_count = 0
    # completed_order_sum = 0
    # cancelled_order_count = 0
    # cancelled_order_sum = 0
    #
    # for order, client_name, client_phone, payment_status, payment_method in orders:
    #     if order.order_status == OrderStatus.completed:
    #         completed_order_count += 1
    #         completed_order_sum += order.total
    #     elif order.order_status == OrderStatus.cancelled:
    #         cancelled_order_count += 1
    #         cancelled_order_sum += order.total
    #     else:
    #         new_order_count += 1
    #         new_order_sum += order.total
    #
    # orders = orders.offset(offset).limit(limit).all()
    #
    # order_list = []
    #
    # for order, client_name, client_phone, payment_status, payment_method in orders:
    #     order = OrderDetailsModel(
    #         id=order.id,
    #         client_name=client_name,
    #         client_phone=client_phone,
    #         products=order.order_items,
    #         total=order.total,
    #         order_status=order.order_status,
    #         payment_status=payment_status,
    #         payment_method=payment_method,
    #         created_at=order.created_at,
    #         updated_at=order.updated_at
    #     )
    #
    #     order_list.append(order)
    #
    # db.close()
    #
    # return {
    #     'orders': order_list,
    #     'new_order_count': new_order_count,
    #     'new_order_sum': new_order_sum,
    #     'completed_order_count': completed_order_count,
    #     'completed_order_sum': completed_order_sum,
    #     'cancelled_order_count': cancelled_order_count,
    #     'cancelled_order_sum': cancelled_order_sum,
    #     'total_count': total_count
    # }


def get_by_id(id: int, db: Session):
    return True
    # order = db.query(OrderDetails, Client.name, Client.phone, PaymentDetails.payment_status,
    #                   PaymentDetails.payment_method) \
    #     .options(selectinload(OrderDetails.order_items)) \
    #     .join(Client, OrderDetails.client_id == Client.id) \
    #     .outerjoin(PaymentDetails, OrderDetails.id == PaymentDetails.order_id) \
    #     .order_by(OrderDetails.id).filter(OrderDetails.id == id).first()
    #
    # if not order:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Order with id {id} not found")
    # one_order = order[0]
    # client_name = order[1]
    # client_phone = order[2]
    # payment_status = order[3]
    # payment_method = order[4]
    #
    # order_list = {
    #     "id": one_order.id,
    #     "client_name": client_name,
    #     "client_phone": client_phone,
    #     "products": one_order.order_items,
    #     "total": one_order.total,
    #     "order_status": one_order.order_status,
    #     "payment_status": payment_status,
    #     "payment_method": payment_method,
    #     "created_at": one_order.created_at,
    #     "updated_at": one_order.updated_at,
    # }
    #
    # db.close()
    # return order_list


def delete(id: int, db: Session):
    return True
    # order_details = db.query(OrderDetails).filter(OrderDetails.id == id)
    # if not order_details.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Order with id {id} not found")
    #
    # order_items = db.query(OrderItems).filter(OrderItems.order_id == id)
    #
    # if order_details.first().order_status == OrderStatus.new:
    #     for order in order_items:
    #         update_product_amount(order.product_id, -order.amount, db)
    #
    # order_items.delete(synchronize_session=False)
    # order_details.delete(synchronize_session=False)
    # db.commit()
    # db.close()
    #
    # return status.HTTP_204_NO_CONTENT
