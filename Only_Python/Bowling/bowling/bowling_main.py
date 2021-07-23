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
    """
    Класс обработки результатов по правилу № 1
    """
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
            if self.rule == LOCAL_RULES:
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
