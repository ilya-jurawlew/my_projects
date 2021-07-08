from datetime import datetime, timedelta

from Only_Python.Weather.weather.models import Weather


class DatabaseUpdater:
    """добавить/получить файл в базу данных"""

    def __init__(self, data_for_save, date_begin, date_end):
        self.data_for_save = data_for_save
        self.date_begin = date_begin
        self.date_end = date_end
        self.beautiful_weather = []

    def get(self):
        d1, d2 = datetime.strptime(self.date_begin, '%Y-%m-%d'), datetime.strptime(self.date_end, '%Y-%m-%d')
        date_range = [(d1 + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, (d2 - d1).days)]
        for date in date_range:
            if Weather.select().where(Weather.date == date):
                weather = Weather.select().where(Weather.date.between(self.date_begin, self.date_end)).tuples()
                return weather

    def save(self):
        for data in self.data_for_save:
            date_format = datetime.strptime(data['date'], '%Y-%m-%d')
            weather, created = Weather.get_or_create(
                date=date_format,
                defaults={'title': data['title'], 'temp_min': data['temp_min'],
                          'temp_max': data['temp_max']})
            if not created:
                query = Weather.update(title=data['title'], temp_min=data['temp_min'],
                                       temp_max=data['temp_max']).where(Weather.id == weather.id)
                query.execute()


# save_weather = DatabaseUpdater(data_for_save=[
#     {'title': 'Переменная облачность, дождь', 'temp_min': '+17', 'temp_max': '+30', 'date': '2021-06-28'},
#     {'title': 'Переменная облачность, мелкий дождь', 'temp_min': '+18', 'temp_max': '+23', 'date': '2021-06-29'},
#     {'title': 'Переменная облачность, мелкий дождь', 'temp_min': '+16', 'temp_max': '+22', 'date': '2021-06-30'},
# ],
#     date_begin=None,
#     date_end=None,
# )
# save_weather.save()
#
# get_weather = DatabaseUpdater(
#     data_for_save=None,
#     date_begin='2021-06-28',
#     date_end='2021-06-30'
# )
#
# for date in get_weather.get():
#     print(date)