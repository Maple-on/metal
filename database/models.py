from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Integer, text, Sequence, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('unique_id', start=10000000, increment=1), primary_key=True, server_default=text("nextval('unique_id')"))
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)


class Verification(Base):
    __tablename__ = 'verifications'

    id = Column(String, nullable=False, primary_key=True)
    code = Column(String, nullable=False)
    status = Column(String, nullable=False, default='Pending')
    created_at = Column(DateTime(timezone=True), default=datetime.now)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, Sequence('unique_id', start=10000000, increment=1), primary_key=True, server_default=text("nextval('unique_id')"))
    username = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)

    order = relationship("Order", back_populates="client")


class Metal(Base):
    __tablename__ = 'metals'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    order = relationship("Order", back_populates="metal")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    metal_id = Column(Integer, ForeignKey("metals.id"))
    metal_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    unit = Column(String, default='m')
    status = Column(String, nullable=False, default='New')
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    client = relationship("Client", back_populates="order")
    metal = relationship("Metal", back_populates="order")


class Banner(Base):
    __tablename__ = 'banners'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    image_url = Column(String, nullable=False)
    forward_url = Column(String, nullable=True)
    desc = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)

