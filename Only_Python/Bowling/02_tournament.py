# -*- coding: utf-8 -*-

# Просчёт протокола турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X

# Выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   winner is Татьяна

# Из текущего файла сделан консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>

import argparse

from Only_Python.Bowling.bowling_handler import bowling_handler


parser = argparse.ArgumentParser(description='bowling_handler')
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()
input_file = args.input
output_file = args.output
bowling_handler.handler(input_file=input_file, output_file=output_file)
