import time
import numpy as np


def start(ctrl, old_word_leds, new_word_leds):
    # Fade new words in
    for j in range(256 / 2):
        ctrl.clear_pixels()
        for i in new_word_leds:
            color = fade(ctrl.color, (j / 256 / 2))
            ctrl.set_pixel(i, color)
        for i in old_word_leds:
            ctrl.set_pixel(i)
        ctrl.show_pixels()
        time.sleep(0.01)

    # Fade old words out
    for j in range(256 / 2):
        ctrl.clear_pixels()
        for i in old_word_leds:
            color = fade(ctrl.color, (1 - j / 256 / 2))
            ctrl.set_pixel(i, color)
        for i in new_word_leds:
            ctrl.set_pixel(i)
        ctrl.show_pixels()
        time.sleep(0.01)

    ctrl.set_pixels(new_word_leds)


def fade(color, percent):
    r = color[0]
    g = color[1]
    b = color[2]

    r = int(max(0, r * percent))
    g = int(max(0, g * percent))
    b = int(max(0, b * percent))

    color = np.array([r, g, b])
    return color
