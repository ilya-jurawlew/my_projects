# -*- coding: utf-8 -*-
import json
import re
import csv
import sys
from decimal import Decimal


remaining_time = '123456.0987654321'
field_names = ['current_location', 'current_experience', 'current_date']

re_location = r'(\w+)_tm(\d+\.?\d*)'
re_mob = r'(\w+)_exp(\d+)_tm(\d+)'


class Warrior:
    def __init__(self):
        self.current_experience = 0
        self.current_date = Decimal('123456.0987654321')
        self.location_name, self.location_time = None, 0
        self.mob_name, self.mob_experience, self.mob_time = None, 0, 0
        self.info = {}

    def edit(self, location=None, mob=None, i=None):
        info = ""
        if location is not None:
            location_info = re.search(re_location, location)
            self.location_name, self.location_time = location_info[1], location_info[2]
            info = self.location_name + ', время перехода ' + str(Decimal(self.location_time)) + ' сек'
            self.info.update({i: {'location_name': self.location_name, 'location_time': self.location_time}})
        if mob is not None:
            mob_info = re.search(re_mob, mob)
            self.mob_name, self.mob_experience, self.mob_time = mob_info[1], mob_info[2], mob_info[3]
            info = self.mob_name + ' - опыт ' + self.mob_experience + ' время убийства - ' + self.mob_time + ' сек'
            self.info.update(
                {i: {'mob_name': self.location_name, 'mob_experience': self.mob_experience, 'mob_time': self.mob_time}})
        return info

    def choice(self, i, insides, data):
        request = int(input('Решай, воин -> '))

        if request >= i:
            print('Надо ввести предложенное число')
            self.choice(i=i, insides=insides, data=data)
        else:
            if type(insides[request]) == str:
                self.current_experience += int(self.info[request]['mob_experience'])
                self.current_date -= Decimal(self.info[request]['mob_time'])
                print('Моб убит, текущий опыт', self.current_experience, ', затраченное время', self.current_date,
                      'сек')
                del insides[request]
                self.act(data=data)
            else:
                self.current_date -= Decimal(self.info[request]['location_time'])
                self.act(data=insides[request])

    def act(self, data):
        while self.current_date >= 0:
            for current_location, insides in data.items():
                if insides:
                    fields = {'current_location': current_location, 'current_experience': self.current_experience,
                              'current_date': self.current_date}

                    with open('dungeon_passage.csv', 'a', newline='') as file:
                        _writer = csv.DictWriter(file, delimiter=',', fieldnames=field_names)
                        _writer.writerow(fields)

                    print('{txt:*^50}'.format(txt='*'), '\nМы сейчас в', self.edit(location=current_location),
                          '\nЗдесь есть:')
                    i = 0
                    for content in insides:
                        if self.location_name == 'Hatch':
                            if self.current_experience >= 200:
                                print('Полная победа!!!')
                                sys.exit()
                            else:
                                print(
                                    'Табличка с надписью: Верным путём шел,'
                                    ' но очков опыта маловато...Попробуй ещё раз!'
                                )
                                return
                        insides_info = [self.edit(mob=content, i=i)] if type(content) == str else [
                            self.edit(location=key, i=i) for key in content]
                        print(insides_info[0], ',      введи', i)
                        i += 1

                    print('У нас опыта', self.current_experience, ', время до наводнения', self.current_date, 'сек')

                    self.choice(i=i, insides=insides, data=data)

                print('идти больше некуда :( придётся начать сначала')
                return
        print('Время вышло :( Поехали ещё раз ')
        return


with open('dungeon_passage.csv', 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(field_names)
while True:
    with open('rpg.json', 'r') as json_file:
        json_data = json.load(json_file)
    warrior = Warrior()
    warrior.act(data=json_data)
