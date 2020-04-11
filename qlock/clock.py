import datetime
import time
import os
import json
import threading

from utils import utils
from web.web import runApp
from config.config import Config
from transition.matrix import matrix

# Depending on the mode import controller
if Config.instance().get()['environment'] == "dev":
    from tests import controller as ct
elif Config.instance().get()['environment'] == "prod":
    from controller import controller as ct

ctrl = ct.Controller()

# check for special dates
def checkdate(now):
    for date in Config.instance().get()['dates']:
        year = now.year
        specialdate = datetime.datetime.strptime(date['date'] + '.' + str(year),'%d.%m.%Y')
        if (specialdate.date() == now.date()):
            return date['text']
    return

# print text
def printText(text):
    words = Config.instance().getWords()
    for char in text:
        print(words['SPECIAL'][char])
        ctrl.turn_on(words['SPECIAL'][char])
        time.sleep(1)

# clock tick
def tick(active_leds):
    time = datetime.datetime.now()
    words = Config.instance().getWords()
    text, new_leds = utils.timeToText(words, time)
    print(text)
    return setTime(active_leds, new_leds)

def setTime(old_leds, new_leds):
    if old_leds == new_leds:
        return old_leds
    new_leds = transition(old_leds, new_leds)

    if old_leds == new_leds:
        return old_leds
        ctrl.turn_on(new_leds)
    return new_leds

def transition(old_leds, new_leds):
    transition = Config.instance().get()['transition']
    if transition == "matrix":
        return matrix(ctrl, old_leds, new_leds)
    return old_leds

if __name__ == "__main__":
    t_webApp = threading.Thread(name='Web App', target=runApp)
    t_webApp.setDaemon(True)
    t_webApp.start()
    
    led = []
    last_special = datetime.datetime.now()
    ctrl.change_color(Config.instance().get()['color'])
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
    