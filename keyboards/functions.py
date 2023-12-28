from constants import PictureStatus

# функция формирования сообшения
def creat_text(users_db, user_id, mode: str, **kwargs) -> str:
    text_name = f'Имя: {users_db[user_id]["name"]}\n' 
    text_contact = f'Телефон: {kwargs.get("enter_telephone", "-")}\n' \
                   f'Способ связи: {kwargs.get("how_contact", "-")}\n'
    text_email = f'Email: {kwargs.get("enter_email", "-")}\n'
    if mode == PictureStatus.READY:
        text_ready = f'Заказ: Готовая картина\n\n' + text_name
        if 'enter_telephone' in kwargs:
            finish_text = text_ready + text_contact
        elif 'enter_email' in kwargs:
            finish_text = text_ready + text_email
    if mode == PictureStatus.ORDER:
        text_order = f'Заказ картины\n\n' + text_name
        text_general = f'Кому картина: {kwargs.get("for_whom", "   ---")}\n' \
                       f'Событие: {kwargs.get("event", "   ---")}\n' \
                       f'Размер: {kwargs.get("size", "   ---")}\n' \
                       f'Настроение: {kwargs.get("mood", "   ---")}\n' \
                       f'Цвета: {kwargs.get("color", "   ---")}'
        if 'enter_telephone' in kwargs:
            finish_text = text_order + text_contact + text_general
        elif 'enter_email' in kwargs:
            finish_text = text_order + text_email + text_general
    return finish_text

