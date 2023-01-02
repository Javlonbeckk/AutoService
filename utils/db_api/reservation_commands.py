from utils.db_api.models import Reservation, Comment, Calendar


async def add_reservation(**kwargs):
    new_reservation = await Reservation(**kwargs).create()
    return new_reservation


async def get_reservation(reservation_id) -> Reservation:
    reservation = await Reservation.query.where(Reservation.id == reservation_id).gino.first()
    return reservation


async def show_reservations():
    return await Reservation.query.distinct(
        Reservation.service,
        Reservation.customer_name,
        Reservation.customer_phone,
        Reservation.date,
        Reservation.time,
        Reservation.price).gino.all()

async def show_users_reservations(id_of_user):
    users_reservations = await Reservation.query.where(Reservation.customer_id == id_of_user).gino.all()
    return users_reservations


async def delete_reservation(reservation_id):
    await Reservation.delete.where(Reservation.id == reservation_id).gino.status()

async def delete_from_calendar(reservation_id):
    date = await Reservation.select('date').where(Reservation.id == reservation_id).gino.scalar()
    time = await Reservation.select('time').where(Reservation.id == reservation_id).gino.scalar()
    selected_date = await Calendar.query.where(Calendar.date == date).gino.first()

    if time == '09:00':
        await selected_date.update(nine="Available").apply()
    if time == '11:00':
        await selected_date.update(eleven="Available").apply()
    if time == '14:00':
        await selected_date.update(two="Available").apply()
    if time == '16:00':
        await selected_date.update(four="Available").apply()



async def add_comment(**kwargs):
    new_comment = await Comment(**kwargs).create()
    return new_comment

async def show_comments():
    return await Comment.query.distinct(
        Comment.comment,
        Comment.date,
        Comment.user_id
    ).gino.all()


async def delete_reservation_bycode(code):
    await Reservation.delete.where(Reservation.code == code).gino.status()

async def get_user_by_reservation_code(code):
    user_id = await Reservation.select('customer_id').where(Reservation.code == code).gino.scalar()
    return user_id

async def get_id_by_code(code):
    id = await Reservation.select('id').where(Reservation.code == code).gino.scalar()
    return id

async def get_user_by_reservation_id(id):
    user_id = await Reservation.select('customer_id').where(Reservation.id == id).gino.scalar()
    return user_id

async def accept_reservation(id):
    reservation = await get_reservation(id)
    await reservation.update(accepted=1).apply()
