import datetime
import time
import os
import json
import threading

from utils import utils
from web.web import runApp
from config.config import Config
from transition.matrix import matrix

opt_address = 0x44
opt_bus = 1
name = 'Clock'

# Depending on the mode import controller
if Config.instance().get()['environment'] == "dev":
    from tests.controller import ws2801 as led_ct
    from tests.controller import opt3001 as opt_ct
elif Config.instance().get()['environment'] == "prod":
    from controller import ws2801 as led_ct
    from controller import opt3001 as opt_ct

led_ctrl = led_ct.Controller()

if Config.instance().get()['opt3001'] == True:
    opt_ctrl = opt_ct.Controller(opt_address, opt_bus)

def checkdate(now):
    """
    Method to check for special dates
    """
    for date in Config.instance().get()['dates']:
        year = now.year
        specialdate = datetime.datetime.strptime(
            date['date'] + '.' + str(year), '%d.%m.%Y')
        if (specialdate.date() == now.date()):
            return date['text']
    return

def printText(text):
    words = Config.instance().getWords()
    for char in text:
        print(words['SPECIAL'][char])
        led_ctrl.turn_on(words['SPECIAL'][char])
        time.sleep(1)

def tick(active_leds):
    config = Config.instance().get()

    # Set new color if exists
    led_ctrl.change_color(config['color'])

    # Adjust brightness
    if config['opt3001'] == True:
        brightness_lux = opt_ctrl.get_brightness()
        brightness_led = utils.calculate_brightness(config, brightness_lux)
        led_ctrl.change_brightness(brightness_led)

    time = datetime.datetime.now()
    words = Config.instance().getWords()
    text, new_leds = utils.timeToText(words, time)
    print(name + ' - ' + text)
    return setTime(active_leds, new_leds)

def setTime(old_leds, new_leds):
    if old_leds == new_leds:
        return old_leds
    new_leds = transition(old_leds, new_leds)

    if old_leds == new_leds:
        return old_leds
        led_ctrl.turn_on(new_leds)
    return new_leds

def transition(old_leds, new_leds):
    transition = Config.instance().get()['transition']
    if transition == "matrix":
        return matrix(led_ctrl, old_leds, new_leds)
    return old_leds


if __name__ == "__main__":
    t_webApp = threading.Thread(name='Web App', target=runApp)
    t_webApp.setDaemon(True)
    t_webApp.start()

    led = []
    last_special = datetime.datetime.now()
    led_ctrl.change_color(Config.instance().get()['color'])
    while True:
        config = Config.instance().get()
        text = checkdate(datetime.datetime.now())
        delta = datetime.datetime.now() - last_special
        if (text and delta.seconds >= config['special_interval']):
            printText(text)
            last_special = datetime.datetime.now()
        else:
            led = tick(led)
            time.sleep(config['tick_interval'])
