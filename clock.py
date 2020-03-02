import datetime
import time
import os
import json
import re
from flask import Flask, request
import threading

from src import controller as ct

global config

with open('word.json', encoding='utf-8') as f:
    words = json.load(f)

with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

ctrl = ct.Controller()

# Starting Flask webapp to configure word clock
def thread_webAPP():
    app = Flask(__name__)
    
    @app.route('/config/set', methods=['POST'])
    def setconfig():
        data = request.get_json()
        string = json.dumps(data)
        with open('config.json', 'w') as f:
            f.write(string)
        return Flask.response_class(status=200)

    @app.route('/config/reload')
    def reload():
        global config
        with open('config.json', encoding='utf-8') as f:
            config = json.load(f)
        return Flask.response_class(status=200)

    app.run(host="0.0.0.0")

# Get actual time in text
def timeToText(time):
    H = time.hour
    M = time.minute

    # Start Text
    text = "ES IST"
    led = [words['TEXT']['ES'], words['TEXT']['IST']]
    minutes = 0

    # Space
    text += " "

    # Minutes
    if 0 <= M < 5:
        text += ""
        minutes = M
    elif 5 <= M < 10 or 55 <= M <= 59:
        text += "FÜNF"
        led.append(words['MINUTES']['FÜNF'])
        if M < 10:
            minutes = M - 5
        else:
            minutes = M - 55
    elif 10 <= M < 15 or 50 <= M < 55:
        text += "ZEHN"
        led.append(words['MINUTES']['ZEHN'])
        if M < 15:
            minutes = M - 10
        else:
            minutes = M - 50
    elif 15 <= M < 20 or 45 <= M < 50:
        text += "VIERTEL"
        led.append(words['MINUTES']['VIERTEL'])
        if M < 20:
            minutes = M - 15
        else: 
            minutes = M - 45
    elif 20 <= M < 25 or 40 <= M < 45:
        text += "ZWANZIG"
        led.append(words['MINUTES']['ZWANZIG'])
        if M < 25:
            minutes = M - 20
        else:
            minutes = M - 40
    elif 25 <= M < 30:
        text += "FÜNF VOR HALB"
        led.append(words['MINUTES']['FÜNF'])
        led.append(words['TEXT']['VOR'])
        led.append(words['TEXT']['HALB'])
        minutes = M - 25
    elif 30 <= M < 35:
        text += "HALB"
        led.append(words['TEXT']['HALB'])
        minutes = M - 30
    elif 35 <= M < 40:
        text += "FÜNF NACH HALB"
        led.append(words['MINUTES']['FÜNF'])
        led.append(words['TEXT']['NACH'])
        led.append(words['TEXT']['HALB'])
        minutes = M - 35 

    # Space
    text += " "

    # Sign
    if 5 <= M < 25:
        text += "NACH"
        led.append(words['TEXT']['NACH'])
    elif 40 <= M <= 59:
        text += "VOR"
        led.append(words['TEXT']['VOR'])

    # Space
    text += " "

    # Hours
    if M >= 25:
        H += 1

    if H > 12:
        H = H - 12

    if H == 1 and M >= 5:
        text += "EINS"
        led.append(words['HOURS']['EINS'])
    if H == 1 and M < 5:
        text += "EIN"
        led.append(words['HOURS']['EIN'])
    elif H == 2:
        text += "ZWEI"
        led.append(words['HOURS']['ZWEI'])
    elif H == 3:
        text += "DREI"
        led.append(words['HOURS']['DREI'])
    elif H == 4:
        text += "VIER"
        led.append(words['HOURS']['VIER'])
    elif H == 5:
        text += "FÜNF"
        led.append(words['HOURS']['FÜNF'])
    elif H == 6:
        text += "SECHS"
        led.append(words['HOURS']['SECHS'])
    elif H == 7:
        text += "SIEBEN"
        led.append(words['HOURS']['SIEBEN'])
    elif H == 8:
        text += "ACHT"
        led.append(words['HOURS']['ACHT'])
    elif H == 9:
        text += "NEUN"
        led.append(words['HOURS']['NEUN'])
    elif H == 10:
        text += "ZEHN"
        led.append(words['HOURS']['ZEHN'])
    elif H == 11:
        text += "ELF"
        led.append(words['HOURS']['ELF'])
    elif H == 12 or H == 0:
        text += "ZWÖLF"
        led.append(words['HOURS']['ZWÖLF'])

    # Space
    text += " "

    # UHR
    if M < 5:
        text += "UHR"
        led.append(words['TEXT']['UHR'])

    # Space
    text += " "

    #Dots
    if minutes == 1:
        text += "PUNKT1"
        led.append(words['MINUTES']['PUNKT1'])
    if minutes == 2:
        text += "PUNKT2"
        led.append(words['MINUTES']['PUNKT2'])
    if minutes == 3:
        text += "PUNKT3"
        led.append(words['MINUTES']['PUNKT3'])
    if minutes == 4:
        text += "PUNKT4"
        led.append(words['MINUTES']['PUNKT4'])

    text = re.sub(' +',' ',text)
    led = [item for sublist in led for item in sublist]
    return text, led

# check fir special dates
def checkdate(now):
    for date in config['dates']:
        year = now.year
        specialdate = datetime.datetime.strptime(date['date'] + '.' + str(year),'%d.%m.%Y')
        if (specialdate.date() == now.date()):
            return date['text']
    return

def tick(text, led):
    time = datetime.datetime.now()
    new_text, new_led = timeToText(time)
    if led != new_led and text != new_text:
        led = new_led
        text = new_text
        ctrl.turn_on(led)
        print(text)
        print(led)
    return text, led

if __name__ == "__main__":
    t_webApp = threading.Thread(name='Web App', target=thread_webAPP)
    t_webApp.setDaemon(True)
    t_webApp.start()
    
    led = []
    text = ""
    ctrl.change_color(config['color'])
    while True:
        text = checkdate(datetime.datetime.now())
        if (text):
            for char in text:
                print(words['SPECIAL'][char])
                ctrl.turn_on(words['SPECIAL'][char])
                time.sleep(1)
            time.sleep(60)
        else:
            text, led = tick(text, led)
            time.sleep(5)
    