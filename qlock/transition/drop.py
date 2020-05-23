import numpy

import utils

def start(ctrl, old_word_leds, new_word_leds):
    # drop words out
    leds = set()
    for step in range(11):
        for word_leds in old_word_leds:
            for led in word_leds:
                x,y = utils.get_xy_led(led)
                led = utils.get_leds_xy(x, y + step)
                leds += led
    
    ctrl.set_pixels(leds)
    

# def start(ctrl, old_word_leds, new_word_leds):
#     # drop words out
#     y_values = set()
#     for word_leds in old_word_leds:
#         for led in word_leds:
#             x,y = utils.get_xy_led(led)
#             y_values.add(y)
    
#     for 

