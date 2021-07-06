import re
import bs4
import requests

re_date = r'(\d+)-(\d+)-(\d+)'
re_title = r'title="(\D+)"(\W){2}img'
re_temp_min = r'мин. <span>(\S\d+)°<'
re_temp_max = r'макс. <span>(\S\d+)°<'


class WeatherMaker:
    """Класс парсинга прогноза, результат возвращает словарь"""

    def __init__(self, city):
        self.city = city
        self.result = []

    def parser(self):
        url = f'https://sinoptik.ua/погода-{self.city}/10-дней'
        response = requests.get(url)
        html = bs4.BeautifulSoup(response.text, features='html.parser')
        weather = html.select('.tabs .main')
        for day in weather:
            day = str(day)
            date = re.search(re_date, day)
            title = re.search(re_title, day)
            temp_min = re.search(re_temp_min, day)
            temp_max = re.search(re_temp_max, day)
            res = {
                'title': title[1],
                'temp_min': temp_min[1],
                'temp_max': temp_max[1],
                'date': date[0],
            }
            self.result.append(res)
        return self.result


# probe = WeatherMaker(city='Москва')
# probe.parser()
