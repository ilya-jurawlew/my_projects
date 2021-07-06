# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно изменить правила подсчета очков в игре.
# "Выходим на внешний рынок, а там правила игры другие!" - сказал он.
#
# Правила подсчета очков изменяются так:
#
# Если во фрейме страйк, сумма очков за этот фрейм будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за два следующих броска шара (в одном или двух фреймах,
# в зависимости от того, был ли страйк в следующем броске).
# Например: первый бросок шара после страйка - тоже страйк, то +10 (сбил 10 кеглей)
# и второй бросок шара - сбил 2 кегли (не страйк, не важно как закончится этот фрейм - считаем кегли) - то еще +2.
#

# Если во фрейме сбит спэр, то сумма очков будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за первый бросок шара в следующем фрейме.
#
# Если фрейм остался открытым, то сумма очков будет равна количеству сбитых кеглей в этом фрейме.
#
# Страйк и спэр в последнем фрейме - по 10 очков.
#
# То есть для игры «Х4/34» сумма очков равна 10+10 + 10+3 + 3+4 = 40,
# а для игры «ХXX347/21» - 10+20 + 10+13 + 10+7 + 3+4 + 10+2 + 3 = 92

# Необходимые изменения сделать во всех модулях. Тесты - дополнить.

# "И да, старые правила должны остаться! для внутреннего рынка..." - уточнил менеджер напоследок.
from abc import ABC, abstractmethod
from contextlib import contextmanager

from lesson_014.bowling import bowling


class GlobalFrameManager(bowling.FrameManager):
    def __init__(self):
        super().__init__()
        self.prev_prev_throw_score = 0
        self.prev_symbol = None
        self.prev_prev_symbol = None

    class FirstThrow(bowling.FrameManager.Throw):
        def strike(self):
            return 10

        def spare(self):
            raise bowling.UnexpectedSymbol(bowling.FrameManager.SPARE_SYMBOL)

    class SecondThrow(bowling.FrameManager.Throw):
        def strike(self):
            raise bowling.UnexpectedSymbol(bowling.FrameManager.STRIKE_SYMBOL)

        def spare(self):
            return 10

    FIRST_THROW = FirstThrow()
    SECOND_THROW = SecondThrow()

    def process(self, symbol):
        is_first_throw = self.current_throw is self.FIRST_THROW
        self.total_frames += is_first_throw

        score = self.current_throw.process(symbol)

        if self.prev_prev_symbol == self.STRIKE_SYMBOL:
            self.total_score += self.prev_throw_score
        elif self.prev_symbol == self.STRIKE_SYMBOL or self.prev_symbol == self.SPARE_SYMBOL:
            self.total_score += score
        self.total_score += score

        if not is_first_throw:
            if symbol == self.SPARE_SYMBOL:
                self.total_score -= self.prev_throw_score
            elif score + self.prev_throw_score >= 10:
                raise bowling.ScoreOverflow()

            self.current_throw = self.FIRST_THROW
        elif symbol != self.STRIKE_SYMBOL:
            self.current_throw = self.SECOND_THROW

        self.prev_prev_symbol = self.prev_symbol
        self.prev_prev_throw_score = self.prev_throw_score

        self.prev_symbol = symbol
        self.prev_throw_score = score


@contextmanager
def game_handler(total_frames=None):
    frame_manager = GlobalFrameManager()
    yield frame_manager
    frame_manager.game_end(total_frames)


def process_game(input_data, total_frames=None):
    with game_handler(total_frames) as frame_manager:
        for symbol in input_data.upper():
            frame_manager.process(symbol)
        print(input_data, frame_manager.total_score)
        return input_data, frame_manager.total_score
# Зачет!