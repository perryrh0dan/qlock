import unittest
import datetime
import utils

import config


class UtilsTests(unittest.TestCase):
    def test_timetotext1(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=23)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZWANZIG NACH ZEHN PUNKT3")

    def test_timetotext2(self):
        words = config.getWords()#
        time = datetime.datetime(year=2020, month=1, day=1, hour=23, minute=59)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST FÜNF VOR ZWÖLF PUNKT4")

    def test_timetotext3(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=10)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZEHN NACH ZWÖLF")

    def test_timetotext4(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=4, minute=00)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST VIER UHR")

    def test_get_leds_xy1(self):
        leds = utils.get_leds_xy(0, 0, 10, "y")
        self.assertEqual(leds, [0, 21, 22, 43, 44, 65, 66, 87, 88, 109])

    def test_get_leds_xy2(self):
        leds = utils.get_leds_xy(10, 0, 10, "y")
        self.assertEqual(leds, [10, 11, 32, 33, 54, 55, 76, 77, 98, 99])

    def test_get_leds_xy3(self):
        leds = utils.get_leds_xy(5, 4, 3, "y")
        self.assertEqual(leds, [49, 60, 71])

if __name__ == "__main__":
    unittest.main()
