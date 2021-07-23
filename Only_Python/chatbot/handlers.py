import re

from generate_ticket import generate_ticket

re_name = re.compile(r'[\w\-\s]{3,40}$')
re_email = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")


def handle_name(text, context):
    """
    Функция-обработчик имени, полученного от пользователя
    :return: True or False
    """
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    """
    Функция-обработчик почты, полученной от пользователя
    :return: True or False
    """
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = text
        return True
    else:
        return False


def generate_ticket_handler(text, context):
    return generate_ticket(name=context['name'], email=context['email'])
