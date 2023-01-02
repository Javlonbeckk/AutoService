from typing import List

from sqlalchemy import and_

from utils.db_api.models import Service, User
from utils.db_api.database import db


# Функция для создания нового товара в базе данных. Принимает все возможные аргументы, прописанные в Item
async def add_service(**kwargs):
    new_service = await Service(**kwargs).create()
    return new_service




# Функция для вывода товаров с РАЗНЫМИ категориями
async def get_categories():
    return await Service.query.distinct(Service.category_name).gino.all()

# Функция для вывода товаров с РАЗНЫМИ подкатегориями в выбранной категории
async def get_subcategories(category):
    return await Service.query.distinct(Service.subcategory_name).where(Service.category_code == category).gino.all()

# Функция вывода всех товаров, которые есть в переданных категории и подкатегории
async def get_services(category_code, subcategory_code):
    service = await Service.query.where(
        and_(Service.category_code == category_code,
             Service.subcategory_code == subcategory_code)
    ).gino.all()
    return service

# Функция для получения объекта товара по его айди
async def get_service(service_id):
    service = await Service.query.where(Service.id == service_id).gino.first()
    return service

async def get_price(service_name):
    price = await Service.select('price').where(Service.name == service_name).gino.scalar()
    return price

async def get_price_en(service_name):
    price = await Service.select('price').where(Service.name_en == f"{service_name}").gino.scalar()
    return price

async def get_price_uz(service_name):
    price = await Service.select('price').where(Service.name_uz == f"{service_name}").gino.scalar()
    return price




