import time
import numpy
from operator import itemgetter

import utils

def start(ctrl, old_word_leds, new_word_leds):
    # drop words out
    leds = []
    if len(old_word_leds) > 0:
        drop_out(ctrl, old_word_leds)

    # drop new words in
    drop_in(ctrl, new_word_leds)

def drop_out(ctrl, target_leds):
    leds = []
    positions = get_positions(target_leds)
    for step in range(11):
        for position in positions:
            led = utils.get_leds_xy(position[0], position[1] + step)
            leds += led
        ctrl.set_pixels(leds)
        leds.clear()
        time.sleep(0.1)

def drop_in(ctrl, target_leds):
    leds = []
    positions = get_positions(target_leds)
    max_y_value = max(positions,key=itemgetter(1))[1]
    for step in range(max_y_value):
        for position in positions:
            led = utils.get_leds_xy(position[0], position[1] - max_y_value + step + 1)
            leds += led
        ctrl.set_pixels(leds)
        leds.clear()
        time.sleep(0.1)


def get_positions(leds):
    positions = set()
    for led in leds:
        positions.add(utils.get_xy_led(led))
    return positions

