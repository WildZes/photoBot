# импортируем ответ пользователю
from settings.message import MESSAGES
from settings import config, utility
# импортируем класс-родитель
from handlers.handler import Handler
from io import BytesIO


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку "Выбрать товар"
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_info(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопоку 'О магазине'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              disable_web_page_preview=True,
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопоку 'Настройки'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              disable_web_page_preview=True,
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_back(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, "Начальное меню",
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопки каталога товаров
        """
        self.bot.send_message(message.chat.id, "Категория " + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ok",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'
        """
        self.step = 0
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(product_id),
                                     self.BD.select_single_product_title(product_id),
                                     self.BD.select_single_product_price(product_id),
                                     self.BD.select_order_quantity(product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keyboards.orders_menu(self.step, quantity))

    def pressed_btn_up(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "UP"
        """
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "DOWN"
        """
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'X' - удалить позицию шага
        """
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            self.BD.delete_order(count[self.step])
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            if self.step > 0:
                self.step -= 1

        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keyboards.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "back_step"
        """
        if self.step > 0:
            self.step -= 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "next_step"
        """
        if self.step < self.BD.count_rows_order()-1:
            self.step += 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_aplly(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Оформить заказ'
        """
        self.bot.send_message(message.chat.id, MESSAGES['apply'].format(
                                                    utility.get_total_cost(self.BD),
                                                    utility.get_total_quantity(self.BD)),
                              parse_mode='HTML', reply_markup=self.keyboards.category_menu())
        self.BD.delete_all_order()

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: message.text != config.KEYBOARD['ADD_PHOTO'] and
                                  message.text != config.KEYBOARD['SEND_ORDER'])
        def handle(message):
            # ********** меню ********** #
            print(message.text)
            if message.text == config.KEYBOARD['SEND_ORDER']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['NAVIGATION']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['PORTFOLIO']:
                photo = self.BD.get_rand_photo()
                self.keyboards.remove = self.bot.send_photo(message.chat.id, BytesIO(photo))
                self.bot.send_message(message.chat.id, 'Выберете категорию работ.',
                                      parse_mode='HTML',
                                      reply_markup=self.keyboards.set_select_category())

            if message.text == config.KEYBOARD['BACK_STEP'] or message.text == config.KEYBOARD['TEST']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keyboards.category_menu())

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            else:
                print(message.text)
                self.bot.send_message(message.chat.id, message.text)
