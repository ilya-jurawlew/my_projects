# -*- coding: utf-8 -*-

from Only_Python.Weather.weather.weather_maker import WeatherMaker
from Only_Python.Weather.weather.image_maker import ImageMaker
from Only_Python.Weather.weather.database_updater import DatabaseUpdater


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
