# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
import json
import re
import csv
import sys
from decimal import Decimal

remaining_time = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
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


# Нужно исправить оформление кода.
with open('dungeon_passage.csv', 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(field_names)
while True:
    with open('rpg.json', 'r') as json_file:
        json_data = json.load(json_file)
    warrior = Warrior()
    warrior.act(data=json_data)

# Учитывая время и опыт, не забывайте о точности вычислений!

# Зачёт!
