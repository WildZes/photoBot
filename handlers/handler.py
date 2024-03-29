# импортируем библиотеку abc для реализации абстрактных классов
import abc
# импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager
from tb_forms import TelebotForms


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keyboards = Keyboards()
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()
        self.tbf = TelebotForms(bot)

    @abc.abstractmethod
    def handle(self):
        pass
