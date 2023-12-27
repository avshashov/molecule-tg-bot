

# функция формирования сообшения
def creat_text(users_db, id, mode: str, **kwargs) -> str:
    if mode == 'ready':
        if 'enter_telephone' in kwargs:
            text = f'Заказ: Готовая картина\n\n' \
                   f'Имя: {users_db[id]["name"]}\n' \
                   f'Телефон: {kwargs["enter_telephone"]}\n' \
                   f'Способ связи: {kwargs["how_contact"]}'

        elif 'enter_email' in kwargs:
            text = f'Заказ: Готовая картина\n\n' \
                   f'Имя: {users_db[id]["name"]}\n' \
                   f'E-mail: {kwargs["enter_email"]}'

    elif mode == 'order':
        if "enter_telephone" in kwargs:
            text = f'Заказ картины\n\n' \
                   f'Имя: {users_db[id]["name"]}\n' \
                   f'Телефон: {kwargs["enter_telephone"]}\n' \
                   f'Способ связи: {kwargs["how_contact"]}\n' \
                   f'Кому картина: {kwargs.get("for_whom", "   ---")}\n' \
                   f'Событие: {kwargs.get("event", "   ---")}\n' \
                   f'Размер: {kwargs.get("size", "   ---")}\n' \
                   f'Настроение: {kwargs.get("mood", "   ---")}\n' \
                   f'Цвета: {kwargs.get("color", "   ---")}'

        elif "enter_email" in kwargs:
            text = f'Заказ картины\n\n' \
                   f'Имя: {users_db[id]["name"]}\n' \
                   f'Email: {kwargs["enter_email"]}\n' \
                   f'Кому картина: {kwargs.get("for_whom", "   ---")}\n' \
                   f'Событие: {kwargs.get("event", "   ---")}\n' \
                   f'Размер: {kwargs.get("size", "   ---")}\n' \
                   f'Настроение: {kwargs.get("mood", "   ---")}\n' \
                   f'Цвета: {kwargs.get("color", "   ---")}'
    return text