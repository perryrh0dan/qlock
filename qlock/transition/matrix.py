import time
import utils
import numpy as np


# def start(ctrl, old_leds, target_leds):
#     while True:
#         new_leds = []
#         for led in old_leds:
#             if led in target_leds:
#                 new_leds.append(led)
#                 continue
#             bLed = getBottomLed(led)
#             if bLed < 111:
#                 new_leds.append(bLed)
#         ctrl.turn_on(new_leds)
#         old_leds = new_leds

#         # Transition is finished if all leds are in target_led
#         if all(elem in target_leds for elem in new_leds):
#             ctrl.turn_on(target_leds)
#             break
#         time.sleep(0.1)

#     return target_leds


def start(ctrl, old_leds, target_leds):
    direction = 'y'
    length = np.random.randint(4, 12, 11)
    length = [ 1, 2, 3, 4, 5, 6, 7, 5, 4, 5, 8]
    max_length = 8

    ctrl.change_color([0, 255, 0])
    for y in range(11 + max_length):
        leds = []
        for x in range(11):
            start_x = x
            start_y = y 
            strip_length = length[x] - ( max_length - y )

            leds = leds + utils.get_leds_xy(start_x, start_y, strip_length, direction)
        time.sleep(1)
        ctrl.turn_on(leds)


def getBottomLed(led):
    return led + 11
