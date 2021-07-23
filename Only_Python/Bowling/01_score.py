# -*- coding: utf-8 -*-
import argparse

from Only_Python.Bowling.bowling import bowling_main


def main():
    """
    Из текущего файла сделана консольная утилита для определения количества очков,
    с помощью пакета argparse.
    Скрипт принимает параметр --result и печататает на консоль
    Количество очков для результатов ХХХ - УУУ.
    """
    parser = argparse.ArgumentParser(description='bowling')
    parser.add_argument('--result', type=str)
    args = parser.parse_args()
    input_data = args.result
    bowling_main.process_game(input_data=input_data, total_frames=10)


if __name__ == '__main__':
    main()

