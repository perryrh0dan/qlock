import json
import time
from src import controller as ct

with open('../word.json', encoding='utf-8') as f:
    words = json.load(f)

text = "HAPPYBIRTHDAY"

ctrl = ct.Controller()

if __name__ == "__main__":
    while True:
        for char in text:
            print(words['SPECIAL'][char])
            ctrl.turn_on(words['SPECIAL'][char])
            time.sleep(1)