import time
import numpy as np

def start(ctrl, old_word_leds, new_word_leds):
    # Fade new words in
    led = old_word_leds + new_word_leds
    colors = np.tile(np.array(ctrl.color), (len(old_word_leds), 1))
    for i in range(10):
        i += 1
        color = fade(ctrl.color, (i / 10))
        colors = np.append(colors, np.tile(np.array(color), (len(new_word_leds), 1)), axis = 0)
        ctrl.set_pixels(led, colors)
        time.sleep(0.05)

    # Fade old words out
    led = new_word_leds + old_word_leds
    colors = np.tile(np.array(ctrl.color), (len(old_word_leds), 1))
    for i in range(10):
        i += 1
        color = fade(ctrl.color, (1 - i/10))
        colors = np.append(colors, np.tile(np.array(color), (len(new_word_leds), 1)), axis = 0)
        ctrl.set_pixels(led, colors)
        time.sleep(0.05)

    ctrl.set_pixels(new_word_leds)

def fade(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([255, 255, 255])
    vector = white-color
    color = color + vector * percent 
    return color.astype(int)
