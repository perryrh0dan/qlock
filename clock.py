import datetime
import time
import os
import json
import threading

from src import utils
from src.web import webApp
from src.config import Config

# Depending on the mode import controller
if Config.instance().get()['environment'] == "dev":
    from tests import controller as ct
elif Config.instance().get()['environment'] == "prod":
    from src import controller as ct

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
def tick(led):
    time = datetime.datetime.now()
    words = Config.instance().getWords()
    text, new_led = utils.timeToText(words, time)
    if led != new_led:
        led = new_led
        ctrl.turn_on(led)
        print(text)
        print(led)
    return led

if __name__ == "__main__":
    t_webApp = threading.Thread(name='Web App', target=webApp)
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
    