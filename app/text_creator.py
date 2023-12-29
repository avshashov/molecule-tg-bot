from app.constants import PictureStatus

# формирование сообшений
class TextCreator:
    
    @staticmethod
    def create_text_ready(users_db, user_id, mode: str, **kwargs) -> str:
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
        return finish_text
    
    @staticmethod
    def create_text_order(users_db, user_id, mode: str, **kwargs) -> str:
        if mode == PictureStatus.ORDER:
            text_name = f'Имя: {users_db[user_id]["name"]}\n' 
            text_contact = f'Телефон: {kwargs.get("enter_telephone", "-")}\n' \
                           f'Способ связи: {kwargs.get("how_contact", "-")}\n'
            text_email = f'Email: {kwargs.get("enter_email", "-")}\n'
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
    
    @staticmethod
    def create_text_rent(users_db, user_id, mode: str, **kwargs) -> str:
        if mode == PictureStatus.RENT:
            text = f'Заказ: Аренда помещения\n\n' \
                   f'Имя: {users_db[user_id]["name"]}\n' \
                   f'Телефон: {kwargs["enter_telephone"]}\n' \
                   f'Способ связи: {kwargs["how_contact"]}\n' \
                   f'Дата: {kwargs["date"]}\n' \
                   f'Мероприятие: {kwargs["event"]}\n' \
                   f'Сколько человек: {kwargs["how_people"]}\n' \
                   f'Залов требуется: {kwargs["how_room"]}'
        return text