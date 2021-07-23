# -*- coding: utf-8 -*-
from contextlib import contextmanager

from Only_Python.Bowling.bowling import bowling_main


class GlobalFrameManager(bowling_main.FrameManager):
    """
    Класс обработки результатов по правилу № 2, наследник правила № 1.
    """
    def __init__(self):
        super().__init__()
        self.prev_prev_throw_score = 0
        self.prev_symbol = None
        self.prev_prev_symbol = None

    class FirstThrow(bowling_main.FrameManager.Throw):
        def strike(self):
            return 10

        def spare(self):
            raise bowling_main.UnexpectedSymbol(bowling_main.FrameManager.SPARE_SYMBOL)

    class SecondThrow(bowling_main.FrameManager.Throw):
        def strike(self):
            raise bowling_main.UnexpectedSymbol(bowling_main.FrameManager.STRIKE_SYMBOL)

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
                raise bowling_main.ScoreOverflow()

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
