from pyparsing import unicode


def format_phone_number(phone_number: str):
    # форматируем под +79999999999
    phone = "".join(x for x in unicode(phone_number) if x in "1234567890")  # убираем лишние символы
    if phone[0] == 8:
        phone = "+" + phone.replace("8", "7", 1)  # заменяем 8 в начале номера на 7

    return phone
