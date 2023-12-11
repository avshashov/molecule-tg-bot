# Демо база данных пользователей
from aiogram.types import InputMediaPhoto

users_db: dict[int, dict] = {}

presentation_id: dict[str, str] = {}
preza = {
    "file_name": "MOLECULE_project.pdf",
    "file_id": "BQACAgIAAxkBAAIB8WVufI2EksKXPy0J4n38Rpkvph9hAAI3QwACRKloS_7fkH536x44MwQ",
    "file_unique_id": "AgADN0MAAkSpaEs",
}


ids = ['AgACAgIAAxkBAAIC1WV2lmH1eN64Zf2GFdDV7yNiyTTlAAI12jEbT-iwS1AKh8QGcFIPAQADAgADeAADMwQ',
            'AgACAgIAAxkBAAIC1mV2lol1_z7KHqlmXaoP4-l-a10yAAI22jEbT-iwS-f6zE4bFrffAQADAgADeAADMwQ',
            'AgACAgIAAxkBAAIC12V2lplmiv8CEcepdNPm6PbrmNlZAAI32jEbT-iwS6ruoiWr1iZqAQADAgADeAADMwQ']

photo_id = [InputMediaPhoto(media=id) for id in ids]
