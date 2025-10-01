import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberMatcher

def extract_and_normalize_phone(text: str):
    """
    Ищет номер телефона в строке, определяет его регион и приводит к международному формату.

    :param text: Строка, содержащая номер телефона
    :return: Отформатированный номер (+77071234567, +996707123456) или None, если номер не найден/некорректен
    """
    try:
        # Ищем номер в тексте
        for i in ['KZ', 'KG']:
            for match in PhoneNumberMatcher(text, i):  # Поиск номеров (по умолчанию KZ)
                parsed_number = match.number

                # Проверка валидности
                if not phonenumbers.is_valid_number(parsed_number):
                    continue

                # Определяем код страны
                country_code = parsed_number.country_code
                national_number = parsed_number.national_number

                # Казахстан (KZ)
                if country_code == 7 and str(national_number).startswith("7"):
                    return f"+{country_code}{national_number}"

                # Кыргызстан (KG)
                if country_code == 996:
                    return f"+{country_code}{national_number}"

                # Если номер с `+` — оставляем, если без `+` и не KZ/KG — игнорируем
                if match.raw_string.startswith("+"):
                    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        return None  # Если номера не нашли
    except NumberParseException as e:
        print(f"Ошибка парсинга: {e}")
        return None