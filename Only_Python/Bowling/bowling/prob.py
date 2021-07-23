# from abc import ABC, abstractmethod
# from contextlib import contextmanager
# import unittest
#
#
# class UnexpectedSymbol(Exception):
#     def __init__(self, symbol):
#         super().__init__()
#         self.symbol = symbol
#
#     def __str__(self):
#         return "Unexpected symbol {}".format(self.symbol)
#
#
# class ScoreOverflow(Exception):
#     def __str__(self):
#         return "Sum of score in one frame is more than 10"
#
#
# class InvalidFramesNumber(Exception):
#     def __str__(self):
#         return "Invalid frames number"
#
#
# class InvalidThrowsNumber(Exception):
#     def __str__(self):
#         return "Invalid throws number"
#
#
# RULE_TYPE_V1 = 'V1'
# RULE_TYPE_V2 = 'V2'
#
# class FrameManager:
#
#     STRIKE_SYMBOL = 'X'
#     SPARE_SYMBOL = '/'
#     MISS_SYMBOL = '-'
#
#     class Throw(ABC):
#         def process(self, symbol):
#             if symbol == FrameManager.STRIKE_SYMBOL:
#                 return self.strike()
#             elif symbol == FrameManager.SPARE_SYMBOL:
#                 return self.spare()
#             elif symbol == FrameManager.MISS_SYMBOL:
#                 score = 0
#             elif '1' <= symbol <= '9':
#                 score = int(symbol)
#             else:
#                 raise UnexpectedSymbol(symbol)
#
#             return score, 0
#
#         @abstractmethod
#         def strike(self):
#             pass
#
#         @abstractmethod
#         def spare(self):
#             pass
#
#     class FirstThrowBase(Throw):
#         MAX_THROWS = 0
#         def spare(self):
#             raise UnexpectedSymbol(FrameManager.SPARE_SYMBOL)
#
#     class SecondThrowBase(Throw):
#         def strike(self):
#             raise UnexpectedSymbol(FrameManager.STRIKE_SYMBOL)
#
#     class FirstThrowV1(FirstThrowBase):
#         def strike(self):
#             return 20, self.MAX_THROWS
#
#     class SecondThrowV1(SecondThrowBase):
#         def spare(self):
#             return 15, 0
#
#     class FirstThrowV2(FirstThrowBase):
#         MAX_THROWS = 2
#         def strike(self):
#             return 10, self.MAX_THROWS
#
#     class SecondThrowV2(SecondThrowBase):
#         def spare(self):
#             return 10, 1
#
#     class ThrowFactoryBase(ABC):
#         @abstractmethod
#         def first_throw(self):
#             pass
#
#         @abstractmethod
#         def second_throw(self):
#             pass
#
#     class ThrowFactoryV1(ThrowFactoryBase):
#         def first_throw(self):
#             return FrameManager.FirstThrowV1()
#
#         def second_throw(self):
#             return FrameManager.SecondThrowV1()
#
#     class ThrowFactoryV2(ThrowFactoryBase):
#         def first_throw(self):
#             return FrameManager.FirstThrowV2()
#
#         def second_throw(self):
#             return FrameManager.SecondThrowV2()
#
#     def __init__(self, rule_type):
#
#         throw_factory = self.ThrowFactoryV1() if rule_type == RULE_TYPE_V1 else self.ThrowFactoryV2()
#         self.first_throw, self.second_throw = throw_factory.first_throw(), throw_factory.second_throw()
#         self.current_throw = self.first_throw
#
#         self.total_frames = 0
#         self.prev_throw_score = 0
#         self.total_score = 0
#         self.throw_number = 0
#         self.throws_buffer = [0] * max(1, self.first_throw.MAX_THROWS)   # cyclic buffer
#
#     def process(self, symbol):
#         idx = self.throw_number % len(self.throws_buffer)
#         is_first_throw = self.current_throw is self.first_throw
#         self.total_frames += is_first_throw
#
#         score, throws_to_add = self.current_throw.process(symbol)
#
#         if not is_first_throw:
#             if symbol == self.SPARE_SYMBOL:
#                 score -= self.prev_throw_score
#             elif score + self.prev_throw_score >= 10:
#                 raise ScoreOverflow()
#
#             self.current_throw = self.first_throw
#         elif symbol != self.STRIKE_SYMBOL:
#             self.current_throw = self.second_throw
#         self.prev_throw_score = score
#
#         self.total_score += score * (self.throws_buffer[idx] + 1)
#
#         self.throws_buffer[idx] = 0
#         self.throw_number += 1
#         for i in range(self.throw_number, self.throw_number + throws_to_add):
#             self.throws_buffer[i % len(self.throws_buffer)] += 1
#
#     def game_end(self, total_frames):
#         if total_frames is not None and total_frames != self.total_frames:
#             raise InvalidFramesNumber()
#
#         if self.current_throw is not self.first_throw:
#             raise InvalidThrowsNumber()
#
#
# @contextmanager
# def game_handler(rule_type, total_frames=None):
#     frame_manager = FrameManager(rule_type)
#     yield frame_manager
#     frame_manager.game_end(total_frames)
#
#
# def process_game(input_data, total_frames=None, rule_type=RULE_TYPE_V1):
#     with game_handler(rule_type, total_frames) as frame_manager:
#         for symbol in input_data.upper():
#             frame_manager.process(symbol)
#
#         return frame_manager.total_score
#
#
# class TestBowlingV1(unittest.TestCase):
#     def test_bad_symbols(self):
#         with self.assertRaises(UnexpectedSymbol):
#             process_game('XXXXXXXXXXXXXa')
#
#         with self.assertRaises(UnexpectedSymbol):
#             process_game('fffff')
#
#     def test_unexpected_symbol(self):
#         with self.assertRaises(UnexpectedSymbol):
#             process_game('123X')
#
#         with self.assertRaises(UnexpectedSymbol):
#             process_game('XX/', 10)
#
#     def test_score_overflow(self):
#         with self.assertRaises(ScoreOverflow):
#             process_game('99', 1)
#
#     def test_invalid_number(self):
#         with self.assertRaises(InvalidFramesNumber):
#             process_game('XXX', 4)
#
#         with self.assertRaises(InvalidThrowsNumber):
#             process_game('X-/118', 4)
#
#     def test_valid_input(self):
#         self.assertEqual(0, process_game(''))
#         self.assertEqual(200, process_game('XXXXXXXXXX', 10))
#         self.assertEqual(75, process_game('1/2/3/4/5/', 5))
#         self.assertEqual(20, process_game('----------X', 6))
#         self.assertEqual(25, process_game('12345/', 3))
#
#
# class TestBowlingV2(unittest.TestCase):
#     def test_valid_input(self):
#         self.assertEqual(0, process_game('', rule_type=RULE_TYPE_V2))
#         self.assertEqual(270, process_game('XXXXXXXXXX', rule_type=RULE_TYPE_V2, total_frames=10))
#         self.assertEqual(64, process_game('1/2/3/4/5/', 5, RULE_TYPE_V2))
#         self.assertEqual(10, process_game('----------X', 6, RULE_TYPE_V2))
#         self.assertEqual(20, process_game('12345/', 3, RULE_TYPE_V2))
#         self.assertEqual(40, process_game('X4/34', 3, RULE_TYPE_V2))
#         self.assertEqual(92, process_game('XXX347/21', 6, RULE_TYPE_V2))
#
#
# if __name__ == '__main__':
#     unittest.main()
