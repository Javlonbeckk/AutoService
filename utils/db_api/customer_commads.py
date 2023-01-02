from typing import List

from sqlalchemy import and_

from utils.db_api.models import User
from utils.db_api.database import db


async def add_customer(**kwargs):
    new_user = await User(**kwargs).create()
    return new_user


async def get_user(user_id) -> User:
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def set_language(user_id, new_language):
    user = await get_user(user_id)
    await user.update(language=new_language).apply()


async def get_language(user_id):
    lang = await User.select('language').where(User.user_id == user_id).gino.scalar()
    return lang
