import unittest

from Only_Python.Bowling.bowling import bowling_main


# new_rules = __import__('03_rules')


class TestBowlingLocal(unittest.TestCase):
    def test_bad_symbols(self):
        with self.assertRaises(bowling_main.UnexpectedSymbol):
            bowling_main.process_game('XXXXXXXXXXXXXa')

        with self.assertRaises(bowling_main.UnexpectedSymbol):
            bowling_main.process_game('fffff')

    def test_unexpected_symbol(self):
        with self.assertRaises(bowling_main.UnexpectedSymbol):
            bowling_main.process_game('123X')

        with self.assertRaises(bowling_main.UnexpectedSymbol):
            bowling_main.process_game('XX/', 10)

    def test_score_overflow(self):
        with self.assertRaises(bowling_main.ScoreOverflow):
            bowling_main.process_game('99', 1)

    def test_invalid_number(self):
        with self.assertRaises(bowling_main.InvalidFramesNumber):
            bowling_main.process_game('XXX', 4)

        with self.assertRaises(bowling_main.InvalidThrowsNumber):
            bowling_main.process_game('X-/118', 4)

    def test_valid_input(self):
        self.assertEqual(('', 0), bowling_main.process_game('', rule=bowling_main.LOCAL_RULES))
        self.assertEqual(('XXXXXXXXXX', 200), bowling_main.process_game('XXXXXXXXXX', 10, bowling_main.LOCAL_RULES))
        self.assertEqual(('1/2/3/4/5/', 75), bowling_main.process_game('1/2/3/4/5/', 5, bowling_main.LOCAL_RULES))
        self.assertEqual(('----------X', 20), bowling_main.process_game('----------X', 6, bowling_main.LOCAL_RULES))
        self.assertEqual(('12345/', 25), bowling_main.process_game('12345/', 3, bowling_main.LOCAL_RULES))


class TestBowlingGlobal(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(('', 0), bowling_main.process_game('', rule=bowling_main.GLOBAL_RULES))
        self.assertEqual(('XXXXXXXXXX', 270), bowling_main.process_game('XXXXXXXXXX', 10, bowling_main.GLOBAL_RULES))
        self.assertEqual(('1/2/3/4/5/', 64), bowling_main.process_game('1/2/3/4/5/', 5, bowling_main.GLOBAL_RULES))
        self.assertEqual(('----------X', 10), bowling_main.process_game('----------X', 6, bowling_main.GLOBAL_RULES))
        self.assertEqual(('12345/', 20), bowling_main.process_game('12345/', 3, bowling_main.GLOBAL_RULES))
        self.assertEqual(('X4/34', 40), bowling_main.process_game('X4/34', 3, bowling_main.GLOBAL_RULES))
        self.assertEqual(('XXX347/21', 92), bowling_main.process_game('XXX347/21', 6, bowling_main.GLOBAL_RULES))


if __name__ == '__main__':
    unittest.main()
