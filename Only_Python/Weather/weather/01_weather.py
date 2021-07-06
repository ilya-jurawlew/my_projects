# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:


# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}
#
# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database

from lesson_016.weather.weather_maker import WeatherMaker
from lesson_016.weather.image_maker import ImageMaker
from lesson_016.weather.database_updater import DatabaseUpdater


class Manager:

    def __init__(self):
        pass

    def act(self):
        choice = int(
            input('Выберите: \n 1 - Добавить прогнозы в БД \n 2 - Получить прогноз \n 3 - Сделать открытку \n'))
        city = input('Какой город?: ').lower()
        if choice == 1:
            self.add_to_bd(city=city)
        elif choice == 2:
            self.get_from_bd()
        elif choice == 3:
            self.to_do_postcard()
        else:
            print('Такого варианта нет(')
            self.act()

    def add_to_bd(self, city):
        weather = WeatherMaker(city=city)
        save_weather = DatabaseUpdater(data_for_save=weather.parser(), date_begin=None, date_end=None)
        save_weather.save()
        print('Прогнозы добавлены')

    def get_from_bd(self):
        date_begin = input('Начальная дата в формате гггг-мм-дд: ')
        self.date_correct(date=date_begin)
        date_end = input('Конечная дата в формате гггг-мм-дд: ')
        self.date_correct(date=date_end)
        get_weather = DatabaseUpdater(data_for_save=None, date_begin=date_begin, date_end=date_end)
        if get_weather.get() is not None:
            for date in get_weather.get():
                date = date[1] + ', Минимум ' + date[2] + ', Максимум ' + date[3] + ', Дата: ' + str(date[4])
                print(date)
        else:
            print('Инфорамции за эти даты у нас нет(')

    def date_correct(self, date):
        date = date.split('-')
        if len(date) == 3 and len(date[0]) == 4 and len(date[1]) == 2 and len(date[2]) == 2:
            return True
        else:
            print('Неверный формат даты')
            self.act()

    def to_do_postcard(self):
        date = input('Дата в формате гггг-мм-дд: ')
        self.date_correct(date=date)
        get_weather = DatabaseUpdater(data_for_save=None, date_begin=date, date_end=date)
        postcard = ImageMaker(data=get_weather.get())
        postcard.view_image()
        print('Открытка сохранена')


manager = Manager()
manager.act()
#зачёт!