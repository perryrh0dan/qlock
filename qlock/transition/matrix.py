import time

import utils

def matrix(ctrl, old_leds, target_leds):
    while True:
        new_leds = []
        for led in old_leds:
            if led in target_leds:
                new_leds.append(led)
                continue
            bLed = getBottomLed(led)
            if bLed < 111:
                new_leds.append(bLed)
        ctrl.turn_on(new_leds)
        old_leds = new_leds
        
        # Transition is finished if all leds are in target_led
        if all(elem in target_leds for elem in new_leds):
            ctrl.turn_on(target_leds)
            break
        time.sleep(0.1)

    return target_leds

def getBottomLed(led):
    return led + 11