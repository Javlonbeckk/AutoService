from typing import List

from sqlalchemy import and_

from utils.db_api.models import Calendar
from utils.db_api.database import db


async def add_new_date(date):
    new_day = await Calendar(date=date).create()
    return new_day


async def get_available_hours(date):
    #selected_date = await Calendar.query.where(Calendar.date==date).gino.first()

    nine = await Calendar.select('nine').where(Calendar.date == date).gino.scalar()
    eleven = await Calendar.select('eleven').where(Calendar.date == date).gino.scalar()
    two = await Calendar.select('two').where(Calendar.date == date).gino.scalar()
    four = await Calendar.select('four').where(Calendar.date == date).gino.scalar()
    arr = [nine, eleven, two, four]
    """
    if nine == "available":
        arr.append("nine")
    if eleven == "available":
        arr.append("eleven")
    if two == "available":
        arr.append("two")
    if four == "available":
        arr.append("four")"""
    return arr


async def get_date(date):
    sdate = await Calendar.query.where(Calendar.date == date).gino.first()
    return sdate

async def brone(date, time):
    selected_date = await get_date(date)
    if time == "09:00":
        await selected_date.update(nine="booked").apply()
    elif time == "11:00":
        await selected_date.update(eleven="booked").apply()
    elif time == "14:00":
        await selected_date.update(two="booked").apply()
    elif time == "16:00":
        await selected_date.update(four="booked").apply()

#async def is_available(date):

async def set_nine(date):
    selected_date = await get_date(date)
    await selected_date.update(nine="Booked").apply()

async def set_eleven(date):
    selected_date = await get_date(date)
    await selected_date.update(eleven="Booked").apply()

async def set_two(date):
    selected_date = await get_date(date)
    await selected_date.update(two="Booked").apply()

async def set_four(date):
    selected_date = await get_date(date)
    await selected_date.update(four="Booked").apply()
