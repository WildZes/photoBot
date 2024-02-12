# импортируем класс родитель
from handlers.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """
        if message.from_user.id == 93365835:
            self.bot.send_message(message.chat.id,
                                  f'{message.from_user.first_name},'
                                  f' - administrator! Пожалуйста, воспользуйтесь меню взаимодействия. \U0001F447',
                                  reply_markup=self.keyboards.admin_menu())
        else:
            self.bot.send_message(message.chat.id,
                                  f'{message.from_user.first_name},'
                                  f' здравствуйте! Пожалуйста, воспользуйтесь меню взаимодействия. \U0001F447',
                                  reply_markup=self.keyboards.start_menu())

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
