import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize
# модуль для работы с токеном
from dotenv import load_dotenv

# токен выдается при регистрации приложения
load_dotenv(".env")
TOKEN = os.getenv('token')
# название БД
NAME_DB = 'photo.db'
# версия приложения
VERSION = '0.0.2'
# автор приложния
AUTHOR = '@wildzes'

# родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'ADD_PHOTO': emojize(':national_park: Добавить фото в БД'),
    'TEST': emojize(':nut_and_bolt: Тест бота'),
    'SEND_ORDER': emojize(':megaphone: Сделать заказ'),
    'INFO': emojize(':speech_balloon: Ваш мастер'),
    'NAVIGATION': emojize(':magnifying_glass_tilted_right: Подсказки'),
    'PORTFOLIO': emojize(":camera_with_flash: Портфолио"),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️'
}

CATEGORY = {
    'ANIMALS': 1,
    'BIJOU': 2,
    'CLOTHES': 3,
    'FOOD': 4,
    'INTERIOR': 5,
    'TOOLS': 6,
    'BEAUTY': 7,
}

RUCAT = {
    'ЖИВОТНЫЕ': 1,
    'УКРАШЕНИЯ': 2,
    'ОДЕЖДА': 3,
    'ЕДА': 4,
    'ИНТЕРЬЕР': 5,
    'ОБОРУДОВАНИЕ': 6,
    'КРАСОТА': 7,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}