# Полезная статья по пагинации
# https://vc.ru/dev/459527-kak-ya-paginaciyu-na-telebot-delal
# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton
# импортируем настройки и утилиты
from settings import config
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Keyboards(metaclass=Singleton):
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()
        self.remove = None

    def set_btn(self, name, step=0, quantity=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """
        if name == "AMOUNT_ORDERS":
            config.KEYBOARD["AMOUNT_ORDERS"] = "{} {} {}".format(step+1, ' из ', str(self.BD.count_rows_order()))

        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = "{}".format(quantity)

        return KeyboardButton(config.KEYBOARD[name])


    def admin_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('ADD_PHOTO')
        itm_btn_2 = self.set_btn('TEST')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        return self.markup

    def start_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('SEND_ORDER')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('PORTFOLIO')
        itm_btn_4 = self.set_btn('NAVIGATION')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3, itm_btn_4)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню 'О магазине'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('BACK_STEP')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кнопок в меню 'Настройки'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('BACK_STEP')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def remove_menu(self):
        """
        Удаляет текущее меню
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок в меню категорий
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    def photo_menu(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.add(InlineKeyboardButton(config.KEYBOARD['BACK_STEP'], callback_data='PREVFOTO'),
                        InlineKeyboardButton(config.KEYBOARD['NEXT_STEP'], callback_data='NEXTFOTO'))
        self.markup.add(InlineKeyboardButton(config.KEYBOARD['X'], callback_data='MAIN'))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self):
        """
        Создает разметку инлайн-кнопок в
        выбранной категории товара и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup()
        buttons = []
        for cat, ind in config.RUCAT.items():
            buttons.append(InlineKeyboardButton(cat, callback_data='CATEGORY'+str(ind)))
        self.markup.add(*buttons)
        self.markup.add(InlineKeyboardButton(config.KEYBOARD['X'], callback_data='MAIN'))
        return self.markup

    def orders_menu(self, step, quantity):
        """
        Создает разметку кнопок в заказе товара и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4 = self.set_btn('UP', step, quantity)
        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)

        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup
