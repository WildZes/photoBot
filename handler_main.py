# импортируем класс HandlerCommands - обработка команд
from handlers.handler_com import HandlerCommands
# импортируем класс HandlerAllText -
# обработка нажатия на кнопки и иные сообщения
from handlers.handler_all_text import HandlerAllText
from handlers.handler_inline_query import HandlerInlineQuery
from handlers.handler_form import HandlerForm


class HandlerMain:
    """
    Класс-компоновщик
    """
    def __init__(self, bot):
        # получаем объект нашего бота
        self.bot = bot
        # здесь будет инициализация обработчиков
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)
        self.handler_form = HandlerForm(self.bot)

    def handle(self):
        # здесь будет запуск обработчиков
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()
        self.handler_form.handle()
