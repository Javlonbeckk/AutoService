from utils.db_api.calendar_commands import add_new_date
from utils.db_api.models import Service
from utils.db_api.service_commands import add_service, get_price
import asyncio

from utils.db_api.database import create_db


async def add_services():
    if await Service.select('name').where(Service.name=="Полировка").gino.scalar() == None:
        await add_service(name="Полировка", name_en="Polishing", name_uz="Polirovka",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                           subcategory_name="Ремонт кузова", subcategory_code="KUZOV",
                          price=77, photo="-")

    if await Service.select('name').where(Service.name == "Покраска").gino.scalar() == None:
        await add_service(name="Покраска", name_en="Painting", name_uz="Rang berish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ремонт кузова", subcategory_code="KUZOV",
                          price=194, photo="-")

    if await Service.select('name').where(Service.name == "Удаление пятен").gino.scalar() == None:
        await add_service(name="Удаление пятен", name_en="Stain Removal", name_uz="Dog`larni ketkazish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ремонт кузова", subcategory_code="KUZOV",
                          price=9, photo="-")

    if await Service.select('name').where(Service.name == "Восстановление кузова").gino.scalar() == None:
        await add_service(name="Восстановление кузова", name_en="Carcase Restoration", name_uz="Kuzovni tiklash",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ремонт кузова", subcategory_code="KUZOV",
                          price=247, photo="-")
    if await Service.select('name').where(Service.name == "Ремонт двигателя").gino.scalar() == None:
        await add_service(name="Ремонт двигателя", name_en="Repair engine", name_uz="Dvigatelni tuzatish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Мотор автомобиля", subcategory_code="MOTOR",
                          price=386, photo="-")

    if await Service.select('name').where(Service.name == "Замена свечей").gino.scalar() == None:
        await add_service(name="Замена свечей", name_en="SP replacement", name_uz="MSH almashtrish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Мотор автомобиля", subcategory_code="MOTOR",
                          price=8, photo="-")

    if await Service.select('name').where(Service.name == "Чистка топливной системы").gino.scalar() == None:
        await add_service(name="Чистка топливной системы", name_en="Cleaning fuel system", name_uz="Yonilgi tizimini tozalash",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Мотор автомобиля", subcategory_code="MOTOR",
                          price=38, photo="-")

    if await Service.select('name').where(Service.name == "Замена технических жидкостей").gino.scalar() == None:
        await add_service(name="Замена технических жидкостей", name_en="TL replacement", name_uz="TSlarni almashtirish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Мотор автомобиля", subcategory_code="MOTOR",
                          price=23, photo="-")

    if await Service.select('name').where(Service.name == "Шлифовка тормозных дисков").gino.scalar() == None:
        await add_service(name="Шлифовка тормозных дисков", name_en="Grinding brake discs", name_uz="Tormoz disklarini silliqlash",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ходовая часть(трансмиссия)", subcategory_code="XODOVAYA",
                          price=30, photo="-")

    if await Service.select('name').where(Service.name == "Ремонт АКПП и МКПП").gino.scalar() == None:
        await add_service(name="Ремонт АКПП и МКПП", name_en="Repair AGB and MGB", name_uz="AUK va MUK;arni tuzatish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ходовая часть(трансмиссия)", subcategory_code="XODOVAYA",
                          price=1, photo="-")

    if await Service.select('name').where(Service.name == "Ремонт амортизатора").gino.scalar() == None:
        await add_service(name="Ремонт амортизатора", name_en="Repair absorber", name_uz="Amortizatorni tuzatish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ходовая часть(трансмиссия)", subcategory_code="XODOVAYA",
                          price=48, photo="-")

    if await Service.select('name').where(Service.name == "Замена амортизатора").gino.scalar() == None:
        await add_service(name="Замена амортизатора", name_en="Replace absorber", name_uz="Amortizatorni almashtirish",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Ходовая часть(трансмиссия)", subcategory_code="XODOVAYA",
                          price=34, photo="-")

    if await Service.select('name').where(Service.name == "Выравнивание давления в шинах").gino.scalar() == None:
        await add_service(name="Выравнивание давления в шинах", name_en="Tire pressure equalization", name_uz="Shina bosimlarini to`girlash",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Вулканизация и Балансировка", subcategory_code="VULBAL",
                          price=17, photo="-")

    if await Service.select('name').where(Service.name == "Вулканизация").gino.scalar() == None:
        await add_service(name="Вулканизация", name_en="Vulcanization", name_uz="Vulkanizatsiya",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Вулканизация и Балансировка", subcategory_code="VULBAL",
                          price=30, photo="-")

    if await Service.select('name').where(Service.name == "Балансировка").gino.scalar() == None:
        await add_service(name="Балансировка", name_en="Balancing", name_uz="Balansirovka",
                          category_name="Ремонт автомобиля", category_code="REMAVTO",
                          subcategory_name="Вулканизация и Балансировка", subcategory_code="VULBAL",
                          price=26, photo="-")

    if await Service.select('name').where(Service.name == "Замена ПО").gino.scalar() == None:
        await add_service(name="Замена ПО", name_en="Replace software", name_uz="Dasturiy ta`minotni almashtirish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Чип-тюнинг", subcategory_code="CHIPTUN",
                          price=57, photo="-")

    if await Service.select('name').where(Service.name == "Оптимизация ПО").gino.scalar() == None:
        await add_service(name="Оптимизация ПО", name_en="Software optimization", name_uz="Dasturiy ta`minotni optimizatsiyalash",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Чип-тюнинг", subcategory_code="CHIPTUN",
                          price=32, photo="-")

    if await Service.select('name').where(Service.name == "Корректировка ПУД").gino.scalar() == None:
        await add_service(name="Корректировка ПУД", name_en="Adjustment EMP", name_uz="DBP ni to`girlash",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Чип-тюнинг", subcategory_code="CHIPTUN",
                          price=69, photo="-")

    if await Service.select('name').where(Service.name == "Установка монитора").gino.scalar() == None:
        await add_service(name="Установка монитора", name_en="Monitor installation", name_uz="Monitor o`rnatish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внутренний тюнинг", subcategory_code="VNUTTUN",
                          price=131, photo="-")

    if await Service.select('name').where(Service.name == "Замена кресел").gino.scalar() == None:
        await add_service(name="Замена кресел", name_en="Replace chairs", name_uz="Kreslolarni almashtirish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внутренний тюнинг", subcategory_code="VNUTTUN",
                          price=46, photo="-")

    if await Service.select('name').where(Service.name == "Установка подсветки").gino.scalar() == None:
        await add_service(name="Установка подсветки", name_en="Ligthing installation", name_uz="Podsvetka o`rnatish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внутренний тюнинг", subcategory_code="VNUTTUN",
                          price=102, photo="-")

    if await Service.select('name').where(Service.name == "Тонирование").gino.scalar() == None:
        await add_service(name="Тонирование", name_en="Toning", name_uz="Tonirovka",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внешний тюнинг", subcategory_code="VNESHTUN",
                          price=30, photo="-")

    if await Service.select('name').where(Service.name == "Установка обвесов").gino.scalar() == None:
        await add_service(name="Установка обвесов", name_en="Installation of carcse kits", name_uz="Kuzov to'plamlarini o'rnatish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внешний тюнинг", subcategory_code="VNESHTUN",
                          price=61, photo="-")

    if await Service.select('name').where(Service.name == "Нанесение рисунка").gino.scalar() == None:
        await add_service(name="Нанесение рисунка", name_en="Painting on a car", name_uz="Rasm chizdirish",
                          category_name="Тюнинг автомобиля", category_code="TUNAVTO",
                          subcategory_name="Внешний тюнинг", subcategory_code="VNESHTUN",
                          price=154, photo="-")



loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_services())



