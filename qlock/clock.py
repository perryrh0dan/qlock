import datetime
import time
import os
import json
import threading

from config import getConfig, getWords
from transition import simple, matrix, fade
import utils

# Depending on the mode import controller
if getConfig()['environment'] == "dev":
    from tests.controller import ws2801 as led_ct
    from tests.controller import opt3001 as opt_ct
elif getConfig()['environment'] == "prod":
    from controller import ws2801 as led_ct
    from controller import opt3001 as opt_ct

name = 'Clock'

led_ctrl = led_ct.Controller()
if getConfig()['opt3001'] == True:
    opt_address = 0x44
    opt_bus = 1
    opt_ctrl = opt_ct.Controller(opt_address, opt_bus)


class Clock(threading.Thread):
    config = None
    active_word_leds = []
    new_word_leds = []
    active_corner_leds = []
    new_corner_leds = []
    last_special = datetime.datetime.now()

    def __init__(self):
        threading.Thread.__init__(self)
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

        self.config = getConfig()
        led_ctrl.change_color(self.config['color'])
        led_ctrl.set_pixels([])

    def run(self):
        """
        Method to run the clock

        """
        while True:
            with self.pause_cond:
                while self.paused:
                    # Turn off leds when paused
                    led_ctrl.set_pixels([])
                    self.pause_cond.wait()
                self.config = getConfig()
                text = self.is_special(datetime.datetime.now())
                delta = datetime.datetime.now() - self.last_special
                if (text and delta.seconds >= self.config['special_interval']):
                    self.display_special(text)
                    self.last_special = datetime.datetime.now()
                else:
                    self.tick()
                    time.sleep(self.config['tick_interval'])
            time.sleep(5)

    def pause(self):
        print(name + ' - Paused')
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    def resume(self):
        print(name + ' - Resumed')
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()

    def tick(self):
        """
        Clock Tick Method

        """
        led_ctrl.change_color(self.config['color'])

        self.check_light_sensor()

        self.generate_leds()

        if self.active_word_leds != self.new_word_leds:
            self.display_words()

        if self.active_corner_leds != self.new_corner_leds:
            self.display_corner()

        self.active_word_leds = self.new_word_leds
        self.active_corner_leds = self.new_corner_leds

    def check_light_sensor(self):
        """ 
        Method to check the light values and to adjust the brightness

        """
        if self.config['opt3001'] == True:
            brightness_lux = opt_ctrl.get_brightness()
            brightness_led = utils.calculate_brightness(
                self.config, brightness_lux)
            led_ctrl.change_brightness(brightness_led)

    def generate_leds(self):
        """
        Method to generate word and corner leds

        """
        time = datetime.datetime.now()
        words = getWords()
        text, self.new_word_leds, self.new_corner_leds = utils.time_to_text(
            words, time)
        print(name + ' - ' + text)

    def display_words(self):
        """
        Method to display word leds

        """
        transition = self.config['transition']
        if transition == "matrix":
            matrix.start(led_ctrl, self.active_word_leds, self.new_word_leds)
        if transition == "fade":
            fade.start(led_ctrl, self.active_word_leds, self.new_word_leds)
        else:
            simple.start(led_ctrl, self.new_word_leds)

    def display_corner(self):
        """
        Method to display corner leds

        """
        for led in self.new_corner_leds:
            led_ctrl.set_pixel(led)
        led_ctrl.show_pixels()

    def display_special(self, text):
        """
        Method to display special dates

        """
        words = getWords()
        for char in text:
            print(words['SPECIAL'][char])
            led_ctrl.set_pixels(words['SPECIAL'][char])
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
