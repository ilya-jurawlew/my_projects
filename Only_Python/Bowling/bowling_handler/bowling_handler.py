from collections import defaultdict

from Only_Python.Bowling.bowling import bowling_main


# new_rules = __import__('03_rules')


class File:
    """
    Запись результатов в файл.
    """
    def __init__(self, input_file, output_file):
        """
        :param input_file: исходный файл
        :param output_file: конечный файл
        """
        self.input_file = input_file
        self.output_file = output_file
        self.result = defaultdict(tuple)

    def rewrite(self):
        with open(self.input_file, mode='r', encoding='utf8') as file_1, \
                open(self.output_file, mode='w', encoding='utf8') as file_2:
            for line in file_1:
                if 'Tour' in line:
                    self.result = defaultdict(tuple)
                    file_2.write(line)
                elif 'winner' in line:
                    for name, score in self.result.items():
                        result = f'{name} {score[0]} {score[1]} \n'
                        file_2.write(result)
                    for name, score in sorted(self.result.items(), key=lambda i: i[1][1], reverse=True)[:1]:
                        file_2.write('winner is ' + name + '\n \n')
                elif not line:
                    continue
                else:
                    try:
                        name, count = line.split()
                    except ValueError as exc:
                        print(f'В строке - {line} ошибка {exc}, введите только имя и результат фрейма')
                    else:
                        try:
                            score = bowling_main.process_game(count)
                            self.result[name] += score
                        except Exception as exc:
                            print(f'Ошибка {exc} в строке {line}')


def handler(input_file, output_file):
    file = File(input_file=input_file, output_file=output_file)
    file.rewrite()
