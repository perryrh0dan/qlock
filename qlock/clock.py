import datetime
import time
import os
import json
import threading

from config import getConfig, getWords
from transition import matrix, simple
import utils

# Depending on the mode import controller
if getConfig()['environment'] == "dev":
    from tests.controller import ws2801 as led_ct
    from tests.controller import opt3001 as opt_ct
elif getConfig()['environment'] == "prod":
    from controller import ws2801 as led_ct
    from controller import opt3001 as opt_ct

opt_address = 0x44
opt_bus = 1
name = 'Clock'

led_ctrl = led_ct.Controller()
if getConfig()['opt3001'] == True:
    opt_ctrl = opt_ct.Controller(opt_address, opt_bus)


class Clock:
    config = None
    active_word_leds = []
    new_word_leds = []
    active_corner_leds = []
    new_corner_leds = []
    last_special = datetime.datetime.now()

    def __init__(self):
        self.config = getConfig()
        led_ctrl.change_color(self.config['color'])
        led_ctrl.turn_on([])

    def start(self):
        while True:
            self.config = getConfig()
            text = self.is_special(datetime.datetime.now())
            delta = datetime.datetime.now() - self.last_special
            if (text and delta.seconds >= self.config['special_interval']):
                self.display_special(text)
                self.last_special = datetime.datetime.now()
            else:
                self.tick()
                time.sleep(self.config['tick_interval'])

    def tick(self):
        # Set new color if exists
        led_ctrl.change_color(self.config['color'])

        self.check_light_sensor()

        self.generate_words()

        if self.active_word_leds != self.new_word_leds:
            transition = self.config['transition']
            if transition == "matrix":
                matrix.start(led_ctrl, self.new_word_leds)
            else:
                simple.start(led_ctrl, self.new_word_leds)

        if self.active_corner_leds != self.new_corner_leds:
            for led in self.new_corner_leds:
                led_ctrl.set_pixel(led)
            led_ctrl.pixels.show()

        self.active_word_leds = self.new_word_leds
        self.active_corner_leds = self.new_corner_leds

    def check_light_sensor(self):
        # Adjust brightness
        if self.config['opt3001'] == True:
            brightness_lux = opt_ctrl.get_brightness()
            brightness_led = utils.calculate_brightness(
                self.config, brightness_lux)
            led_ctrl.change_brightness(brightness_led)

    def generate_words(self):
        time = datetime.datetime.now()
        words = getWords()
        text, self.new_word_leds, self.new_corner_leds = utils.time_to_text(words, time)
        print(name + ' - ' + text)

    def display_special(self, text):
        words = getWords()
        for char in text:
            print(words['SPECIAL'][char])
            led_ctrl.turn_on(words['SPECIAL'][char])
            time.sleep(1)

    def is_special(self, now):
        """
        Method to check for special dates

        """
        for date in self.config['dates']:
            year = now.year
            specialdate = datetime.datetime.strptime(
                date['date'] + '.' + str(year), '%d.%m.%Y')
            if (specialdate.date() == now.date()):
                return date['text']
        return


if __name__ == "__main__":
    clock = Clock()
    clock.start()
