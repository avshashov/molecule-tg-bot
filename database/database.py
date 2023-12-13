# Демо база данных пользователей
from aiogram.types import InputMediaPhoto

# Шаблон заполнения
users_db_template = {
    'user_id': {
        'name': 'user_name',
    }
}

users_db: dict[int, dict] = {}

presentation_id: dict[str, str] = {}
preza = {
    "file_name": "MOLECULE_project.pdf",
    "file_id": "BQACAgIAAxkBAAIB8WVufI2EksKXPy0J4n38Rpkvph9hAAI3QwACRKloS_7fkH536x44MwQ",
    "file_unique_id": "AgADN0MAAkSpaEs",
}


ids_photo_room = ['AgACAgIAAxkBAAIFXGV5WzWSM0w3z2U_JS04MIbEbAqkAAIC1DEbc5vRSwKSB3ZHkHHnAQADAgADeAADMwQ',
                  'AgACAgIAAxkBAAIFXWV5W0dZ4hl14KLej1pmGZw_AAFHFgACA9QxG3Ob0UvfJ6tSAsBDJQEAAwIAA3gAAzME',
                  'AgACAgIAAxkBAAIFXmV5W1AzsgvM_0XycqOouFJE5jTmAAIE1DEbc5vRS4bjuxPNybAnAQADAgADeAADMwQ',
                  'AgACAgIAAxkBAAIFX2V5W1Ybj8uZgY3nl_NUREARkf6LAAIF1DEbc5vRS2JOJXGW6CFwAQADAgADeAADMwQ',
                  'AgACAgIAAxkBAAIFYGV5W1pXcMLeNq1iD4-TCyv-KwKlAAIG1DEbc5vRSxmrshQKhRZ-AQADAgADeAADMwQ',
                  'AgACAgIAAxkBAAIFYWV5W14GL_5sEzngEdmZ3kWrqF0kAAII1DEbc5vRS3HGXfv6xIPeAQADAgADeAADMwQ',
                  'AgACAgIAAxkBAAIFYmV5W2NwI7wHlYXLG4GCojtyqlCJAAIJ1DEbc5vRS-fNt42_9O2vAQADAgADeAADMwQ']

photo_room = [InputMediaPhoto(media=id) for id in ids_photo_room]
