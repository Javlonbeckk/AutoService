import asyncio

from gino.schema import GinoSchemaVisitor

from data.config import POSTGRES_URI
from utils.db_api.database import create_db, db

from utils.db_api.add_to_database import add_services



async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await create_db()



    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()


    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(create_db())
    #loop.run_until_complete(add_items())



if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
