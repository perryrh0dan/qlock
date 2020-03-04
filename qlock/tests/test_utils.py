import unittest
import datetime
from utils import utils

from config.config import Config

class UtilsTests(unittest.TestCase):
    def test_timetotext1(self):
        words = Config.instance().getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 10, minute = 23)
        text, led = utils.timeToText(words, time)
        self.assertEqual(text, "ES IST ZWANZIG NACH ZEHN PUNKT3")

    def test_timetotext2(self): 
        words = Config.instance().getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 23, minute = 59)
        text, led = utils.timeToText(words, time)
        self.assertEqual(text, "ES IST FÜNF VOR ZWÖLF PUNKT4")

    def test_timetotext3(self): 
        words = Config.instance().getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 10)
        text, led = utils.timeToText(words, time)
        self.assertEqual(text, "ES IST ZEHN NACH ZWÖLF")

    def test_timetotext4(self): 
        words = Config.instance().getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 4, minute = 00)
        text, led = utils.timeToText(words, time)
        self.assertEqual(text, "ES IST VIER UHR")

if __name__ == "__main__":
    unittest.main()
