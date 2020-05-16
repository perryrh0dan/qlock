import unittest
import datetime
from utils import utils

import config.config

class UtilsTests(unittest.TestCase):
    def test_timetotext1(self):
        words = config.getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 10, minute = 23)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZWANZIG NACH ZEHN PUNKT3")

    def test_timetotext2(self): 
        words = config.getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 23, minute = 59)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST FÜNF VOR ZWÖLF PUNKT4")

    def test_timetotext3(self): 
        words = config.getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 10)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST ZEHN NACH ZWÖLF")

    def test_timetotext4(self): 
        words = config.getWords()
        time = datetime.datetime(year = 2020, month = 1, day = 1, hour = 4, minute = 00)
        text, led = utils.time_to_text(words, time)
        self.assertEqual(text, "ES IST VIER UHR")

if __name__ == "__main__":
    unittest.main()
