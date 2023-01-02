from sqlalchemy import (Column, Integer, String, Sequence, BigInteger)
from sqlalchemy import sql
from utils.db_api.database import db


class Service(db.Model):
    __tablename__ = "services"
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    category_code = Column(String(20))
    category_name = Column(String(50))

    subcategory_code = Column(String(20))
    subcategory_name = Column(String(50))

    name = Column(String(50))
    name_en = Column(String(50))
    name_uz = Column(String(50))

    photo = Column(String(250))
    price = Column(Integer)

    def __repr__(self):
        return f"""
    Товар № {self.id} - "{self.name}"
    Цена: {self.price}"""


class Reservation(db.Model):
    __tablename__ = "reservations"
    query: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    code = Column(String(100))
    customer_id = Column(BigInteger())
    customer_name = Column(String(100))
    customer_phone = Column(String(13))
    service = Column(String(50))
    date = Column(String(10))
    time = Column(String(5))
    price = Column(Integer)
    accepted = Column(Integer)



class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    user_id = Column(BigInteger(), primary_key=True)
    fullname = Column(String(100))
    username = Column(String(50))
    language = Column(String(2), default="ru")


class Calendar(db.Model):
    __tablename__ = "calendar"
    query: sql.Select

    date = Column(String(10), primary_key=True)
    nine = Column(String(20), default="Available")
    eleven = Column(String(20), default="Available")
    two = Column(String(20), default="Available")
    four = Column(String(20), default="Available")

class Comment(db.Model):
    __tablename__ = "comments"
    query: sql.Select

    date = Column(String(10))
    user_id = Column(BigInteger())
    comment = Column(String())