# -*- coding: utf-8 -*-
import argparse

from Only_Python.Bowling.bowling_handler import bowling_handler


def main():
    """
    Из текущего файла сделан консольный скрипт для формирования файла с результатами турнира.
    Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>
    """
    parser = argparse.ArgumentParser(description='bowling_handler')
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    bowling_handler.handler(input_file=input_file, output_file=output_file)


if __name__ == '__main__':
    main()
