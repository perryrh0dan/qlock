import unittest
import datetime
import utils

import config


class UtilsTests(unittest.TestCase):
    def test_timetotext1(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=23)
        text, word_leds, corner_leds = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZWANZIG NACH ZEHN PUNKT3")

    def test_timetotext2(self):
        words = config.getWords()#
        time = datetime.datetime(year=2020, month=1, day=1, hour=23, minute=59)
        text, word_leds, corner_leds = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST FÜNF VOR ZWÖLF PUNKT4")

    def test_timetotext3(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=10)
        text, word_leds, corner_leds = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZEHN NACH ZWÖLF")

    def test_timetotext4(self):
        words = config.getWords()
        time = datetime.datetime(year=2020, month=1, day=1, hour=4, minute=00)
        text, word_leds, corner_leds = utils.time_to_text(words, time)
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

    def test_get_leds_xy4(self):
        leds = utils.get_leds_xy(5, 3, 5, "y")
        self.assertEqual(leds, [38, 49, 60, 71, 82])

    def test_get_leds_xy5(self):
        leds = utils.get_leds_xy(6, 3, 6, "y")
        self.assertEqual(leds, [37, 50, 59, 72, 81, 94])

    def test_get_xy_led1(self):
        x,y = utils.get_xy_led(11)
        self.assertEqual(x, 10)
        self.assertEqual(y, 1)

    def test_get_xy_led2(self):
        x,y = utils.get_xy_led(12)
        self.assertEqual(x, 9)
        self.assertEqual(y, 1)

    def test_get_xy_led3(self):
        x,y = utils.get_xy_led(22)
        self.assertEqual(x, 0)
        self.assertEqual(y, 2)

    def test_get_xy_led4(self):
        x,y = utils.get_xy_led(69)
        self.assertEqual(x, 3)
        self.assertEqual(y, 6)

    def test_get_xy_led5(self):
        x,y = utils.get_xy_led(99)
        self.assertEqual(x, 10)
        self.assertEqual(y, 9)
        
    def test_get_xy_led6(self):
        x,y = utils.get_xy_led(10)
        self.assertEqual(x, 10)
        self.assertEqual(y, 0)
if __name__ == "__main__":
    unittest.main()
