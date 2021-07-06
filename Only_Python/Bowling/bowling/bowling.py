from abc import ABC, abstractmethod
from contextlib import contextmanager


class UnexpectedSymbol(Exception):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def __str__(self):
        return "Unexpected symbol {}".format(self.symbol)


class ScoreOverflow(Exception):
    def __str__(self):
        return "Sum of score in one frame is more than 10"


class InvalidFramesNumber(Exception):
    def __str__(self):
        return "Invalid frames number"


class InvalidThrowsNumber(Exception):
    def __str__(self):
        return "Invalid throws number"


GLOBAL_RULES = 'global'
LOCAL_RULES = 'local'


class FrameManager:

    STRIKE_SYMBOL = 'X'
    SPARE_SYMBOL = '/'
    MISS_SYMBOL = '-'

    class Throw(ABC):
        def process(self, symbol):
            if symbol == FrameManager.STRIKE_SYMBOL:
                return self.strike()
            elif symbol == FrameManager.SPARE_SYMBOL:
                return self.spare()
            elif symbol == FrameManager.MISS_SYMBOL:
                return 0
            elif '1' <= symbol <= '9':
                return int(symbol)
            else:
                raise UnexpectedSymbol(symbol)

        @abstractmethod
        def strike(self):
            pass

        @abstractmethod
        def spare(self):
            pass

    class FirstThrow(Throw):
        def __init__(self, rule):
            self.rule = rule

        def strike(self):
            if self.rule == LOCAL_RULES:  # вот что бы эти проверки не были разбросанв по коду
                # и нужна иерархия классов и шаблон абстрактная фабрика.
                # В моем решение правило проверяется только один раз...
                return 20
            elif self.rule == GLOBAL_RULES:
                return 10

        def spare(self):
            raise UnexpectedSymbol(FrameManager.SPARE_SYMBOL)

    class SecondThrow(Throw):
        def __init__(self, rule):
            self.rule = rule

        def strike(self):
            raise UnexpectedSymbol(FrameManager.STRIKE_SYMBOL)

        def spare(self):
            if self.rule == LOCAL_RULES:
                return 15
            elif self.rule == GLOBAL_RULES:
                return 10

    def __init__(self, rule):
        self.SECOND_THROW = self.SecondThrow(rule)
        self.FIRST_THROW = self.FirstThrow(rule)
        self.current_throw = self.FIRST_THROW
        self.total_frames = 0
        self.prev_throw_score = 0
        self.total_score = 0
        self.prev_prev_throw_score = 0
        self.prev_symbol = 0
        self.prev_prev_symbol = 0
        self.rule = rule

    def process(self, symbol, rule):
        is_first_throw = self.current_throw is self.FIRST_THROW
        self.total_frames += is_first_throw

        score = self.current_throw.process(symbol)

        if self.rule == GLOBAL_RULES:
            if symbol == self.SPARE_SYMBOL:
                score = score - self.prev_throw_score
            if self.prev_prev_symbol == self.STRIKE_SYMBOL:
                self.total_score += score
            if self.prev_symbol == self.SPARE_SYMBOL or self.prev_symbol == self.STRIKE_SYMBOL:
                self.total_score += score
        self.total_score += score

        if not is_first_throw:
            if self.rule == LOCAL_RULES and symbol == self.SPARE_SYMBOL:
                self.total_score -= self.prev_throw_score
            if symbol != self.SPARE_SYMBOL and score + self.prev_throw_score >= 10:
                raise ScoreOverflow()

            self.current_throw = self.FIRST_THROW
        elif symbol != self.STRIKE_SYMBOL:
            self.current_throw = self.SECOND_THROW

        if self.rule == GLOBAL_RULES:
            self.prev_prev_symbol = self.prev_symbol
            self.prev_prev_throw_score = self.prev_throw_score
            self.prev_symbol = symbol
        self.prev_throw_score = score

    def game_end(self, total_frames):
        if total_frames is not None and total_frames != self.total_frames:
            raise InvalidFramesNumber()

        if self.current_throw is not self.FIRST_THROW:
            raise InvalidThrowsNumber()


@contextmanager
def game_handler(rule, total_frames=None):
    frame_manager = FrameManager(rule)
    yield frame_manager
    frame_manager.game_end(total_frames)


def process_game(input_data, total_frames=None, rule=GLOBAL_RULES):
    with game_handler(rule, total_frames) as frame_manager:
        for symbol in input_data.upper():
            frame_manager.process(symbol, rule)
        print(input_data, frame_manager.total_score)
        return input_data, frame_manager.total_score

# def get_score(game_result):
#     yyy = []
#     frames = []
#     throw = 0
#     for element in game_result:
#         throw += 1
#         if element == 'X':
#             frames.append(1)
#             yyy.append(20)
#         elif element == '-':
#             frames.append(0.5)
#             yyy.append(0)
#         elif element == '/':
#             frames.pop(throw - 2)
#             frames.append(1)
#             throw -= 1
#             yyy.pop(throw-1)
#             yyy.append(15)
#         elif element.isdigit(): # проверка на число
#             frames.append(0.5)
#             yyy.append(int(element))
#             # if ...... : # если сейчас второй бросок во фрейме
#             #     if yyy[throw-1] + yyy[prev_throw] >=10:
#             #         raise ValueError('Многовато кеглей, друг...')
#             # prev_throw = throw
#         else:
#             raise ValueError(f'Недопустимый элемент - {element}') # проверка на лишние буквы
#     if float(sum(frames)) == 10.0: # проверка количества фреймов, бросков и правильность ввода (исключает фрейм '/1' и т.п.)
#         print(game_result, '-', sum(yyy), yyy)
#     else:
#         raise ValueError('У нас тут десять фреймов, ни больше ни меньше')
#
#
# if __name__ == '__main__':
#     res = 'XX55XXXXXXX' #
#
#     print(get_score(res))


# class Bowling:
#     def __init__(self, *args, **kwargs):
#         self.count = 0
#         self.result = ''
#
#     def frame(self):
#         throw_1 = random.randint(0, 10)
#         if throw_1 == 10:
#             self.result = 'X'
#             self.count = 20
#         else:
#             if throw_1 == 0:
#                 self.result = '-'
#             else:
#                 self.result = str(throw_1)
#             self.count = throw_1
#             balance = 10 - throw_1
#             throw_2 = random.randint(0, balance)
#             if throw_2 == balance:
#                 self.count = 15
#                 self.result += '/'
#             elif throw_2 == 0:
#                 self.result += '-'
#             else:
#                 self.count += throw_2
#                 self.result += str(throw_2)
#
#         return self.result, self.count
#
#
# if __name__ == '__main__':
#     def game_result():
#         xxx = []
#         yyy = []
#         res = []
#         for batch in range(10):
#             game = Bowling()
#             res.append(game.frame())
#         for cipher, count in res:
#             xxx.append(cipher)
#             yyy.append(count)
#
#         game_res = ''.join(xxx), '-', sum(yyy)
#         print(game_res)
#         return game_res
#
#
#     game_result()

# count = 0
# result = ''


# def game_result():  # ещё в таком стиле сделал
#     xxx = []
#     yyy = []
#
#     def frame():
#         throw_1 = random.randint(0, 10)
#         if throw_1 == 10:
#             result = 'X'
#             count = 20
#         else:
#             if throw_1 == 0:
#                 result = '-'
#             else:
#                 result = str(throw_1)
#             count = throw_1
#             balance = 10 - throw_1
#             throw_2 = random.randint(0, balance)
#             if throw_2 == balance:
#                 count = 15
#                 result += '/'
#             elif throw_2 == 0:
#                 result += '-'
#             else:
#                 count += throw_2
#                 result += str(throw_2)
#
#         xxx.append(result)
#         yyy.append(count)
#
#     [frame() for _ in range(10)]
#     game_res = ''.join(xxx), '-', sum(yyy)
#     print(game_res)
#     return game_res
#
# game_result()
#
#
# def get_score(game_res):  # что-то такое должно быть? ?
#     try:
#         len(game_res) > 1
#     except ValueError:
#         print('Должно быть число число!')
#     except IndexError:
#         print('Подозрительно мало очков...')
#     except BaseException:
#         print('Что-то пошло не так')
