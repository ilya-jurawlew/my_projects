# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

import os
from PIL import Image, ImageDraw, ImageFont, ImageColor


class TicketMaker: # тут всё прям по аналогии с практикой)

    def __init__(self, fio, from_, to, date):
        self.fio = fio
        self.from_ = from_
        self.to = to
        self.date = date
        self.template = 'images/ticket_template.png'
        self.font_path = os.path.join('fonts', 'ofont.ru_SonyEricssonLogo.ttf')

    def make_ticket(self):
        blank = Image.open(self.template)
        draw = ImageDraw.Draw(blank)
        font = ImageFont.truetype(self.font_path, size=17)

        y = blank.size[1] - 280
        message = f'{self.fio}'
        draw.text((50, y), message, font=font, fill=ImageColor.colormap['black'])

        y = blank.size[1] - 210
        message = f'{self.from_}'
        draw.text((50, y), message, font=font, fill=ImageColor.colormap['black'])

        y = blank.size[1] - 145
        message = f'{self.to}'
        draw.text((50, y), message, font=font, fill=ImageColor.colormap['black'])

        y = blank.size[1] - 145
        message = f'{self.date}'
        draw.text((290, y), message, font=font, fill=ImageColor.colormap['black'])

        # blank.show()
        out_path = 'images/new_ticket.jpg'
        blank.save(out_path)


if __name__ == '__main__':
    fio = input('Введите ФИО: ')
    from_ = input('Город отправления: ')
    to = input('Город прибытия: ')
    date = input('Дата вылета: ')
    ticket = TicketMaker(fio=fio, from_=from_, to=to, date=date)
    ticket.make_ticket()

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
# Зачет!