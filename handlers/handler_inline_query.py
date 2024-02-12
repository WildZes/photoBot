from handlers.handler import Handler
from settings.message import MESSAGES
from settings import utility
from io import BytesIO


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлай-кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.number = 0
        self.cat_img = []

    def pressed_btn_product(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие инлайн-кнопок товара
        """
        self.BD._add_orders(1, code, 1)

        self.bot.answer_callback_query(
            call.id,
            MESSAGES['product_order'].format(
                self.BD.select_single_product_name(code),
                self.BD.select_single_product_title(code),
                self.BD.select_single_product_price(code),
                self.BD.select_single_product_quantity(code)),
            show_alert=True)

    def handle(self):
        """
        Обработчик(декоратор) запросов от нажатия на кнопки товара
        """
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
                self.pressed_btn_product(call, code)
            if 'CATEGORY' in call.data:
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.bot.delete_message(call.message.chat.id, self.keyboards.remove.message_id)
                self.cat_img = self.BD.get_images_by_category(int(''.join(filter(str.isdigit, call.data))))
                self.keyboards.remove = self.bot.send_photo(call.message.chat.id, BytesIO(self.cat_img[0].img))
                self.bot.send_message(call.message.chat.id, 'Воспользуйтесь меню просмотра.',
                                      parse_mode='HTML',
                                      reply_markup=self.keyboards.photo_menu())
            if call.data == 'NEXTFOTO':
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.bot.delete_message(call.message.chat.id, self.keyboards.remove.message_id)
                self.number += 1
                if self.number >= self.cat_img.count():
                    self.number = 0
                self.keyboards.remove = self.bot.send_photo(call.message.chat.id, BytesIO(self.cat_img[self.number].img))
                self.bot.send_message(call.message.chat.id, 'Воспользуйтесь меню просмотра.',
                                      parse_mode='HTML',
                                      reply_markup=self.keyboards.photo_menu())
            if call.data == 'PREVFOTO':
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.bot.delete_message(call.message.chat.id, self.keyboards.remove.message_id)
                self.number -= 1
                if self.number < 0:
                    self.number = self.cat_img.count() - 1
                self.keyboards.remove = self.bot.send_photo(call.message.chat.id, BytesIO(self.cat_img[self.number].img))
                self.bot.send_message(call.message.chat.id, 'Воспользуйтесь меню просмотра.',
                                      parse_mode='HTML',
                                      reply_markup=self.keyboards.photo_menu())
            if call.data == 'MAIN':
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.bot.delete_message(call.message.chat.id, self.keyboards.remove.message_id)
                self.number = 0
                self.bot.send_message(call.message.chat.id, "Начальное меню",
                                      reply_markup=self.keyboards.start_menu())
