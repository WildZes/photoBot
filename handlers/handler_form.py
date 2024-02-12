from datetime import datetime
from io import BytesIO

from handlers.handler import Handler
from settings import config
from models.image import Image
from models.order_photo import Orders
from tb_forms import BaseForm, fields


class HandlerForm(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    def handle(self):
        @self.bot.message_handler(func=lambda message: message.text == config.KEYBOARD['ADD_PHOTO'] or
                                  message.text == config.KEYBOARD['SEND_ORDER'])
        def handle(message):
            if message.text == config.KEYBOARD['ADD_PHOTO']:
                self.tbf.send_form(message.chat.id, AddPhotoForm())
            if message.text == config.KEYBOARD['SEND_ORDER']:
                self.tbf.send_form(message.chat.id, AddOrderForm())


        @self.tbf.form_submit_event("ADD_PHOTO")
        def submit_register_update(call, form_data):
            file_info = self.bot.get_file(form_data.photo.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            image = Image(data=datetime.now(), img=downloaded_file, category_id=config.CATEGORY[form_data.category])
            self.BD.get_session().add(image)
            self.BD.get_session().commit()
            self.BD.close()
            self.bot.send_message(call.message.chat.id, "Фото добавлено")
            self.bot.send_message(call.message.chat.id,
                                  f'Пожалуйста, воспользуйтесь меню взаимодействия. \U0001F447',
                                  reply_markup=self.keyboards.admin_menu())

        @self.tbf.form_submit_event("ADD_ORDER")
        def submit_order(call, form_data):
            if form_data.photo is not None:
                file_info = self.bot.get_file(form_data.photo.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
            else:
                downloaded_file = None
            order = Orders(name=form_data.thing, description=form_data.short, photo=downloaded_file, about_contact=form_data.method,
                           contact=form_data.contact, data=datetime.now())
            self.BD.get_session().add(order)
            self.BD.get_session().commit()
            self.BD.close()
            # Sdelat' kanal dlya zakazov kuda prisilat' tekuschie zakazi
            self.bot.send_message(call.message.chat.id, "Спасибо за заказ с Вами свяжутся в ближайшее время.")
            if downloaded_file:
                self.bot.send_photo(-1001824803203, BytesIO(downloaded_file))
            self.bot.send_message(-1001824803203, f'Предмет: {form_data.thing}\nОписание:\n{form_data.short}\n'
                                                  f'Для свяизи: {form_data.method}\nКонтакт: {form_data.contact}')


class AddPhotoForm(BaseForm):
    update_name = "ADD_PHOTO"
    form_title = "Please fill this form."
    category = fields.ChooseField("Доступные категории", "Выберите одну из доступных категорий или добавьте категорию из"
                                                         " меню администратора", answer_list=list(config.CATEGORY.keys()))
    photo = fields.MediaField(
        "Фото", "Загрузите фото:",
        valid_types=['photo'], required=False, error_message="Error. You can only send a photo")
    freeze_mode = True
    close_form_but = True
    submit_button_text = "Добавить"


class AddOrderForm(BaseForm):
    update_name = "ADD_ORDER"
    form_title = "Для заказа необходимо заполнить следующие поля:"
    thing = fields.StrField("Название", "Укажите название предмета(-ов).")
    short = fields.StrField("Краткое описание", "Кратко опишите предмет(-ы)")
    photo = fields.MediaField(
        "Фото (по желанию)", "Загрузить фото:",
        valid_types=['photo'], required=False, error_message="Error. You can only send a photo")
    method = fields.ChooseField("Способ связи", "Выберете более удобный тип связи:",
                                answer_list=["Телефон", "Почта", "Telegram", "WhatsApp", "Viber", "Other"])
    contact = fields.StrField("Контактная информация", "Укажите контактную информацию")
    freeze_mode = True
    close_form_but = False
    submit_button_text = "Отправить"
