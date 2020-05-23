import time
import numpy as np


def start(ctrl, old_word_leds, new_word_leds):
    # Fade new words in
    for j in range(128):
        ctrl.clear_pixels()
        for i in new_word_leds:
            color = get_color(ctrl.color, (j / 128))
            ctrl.set_pixel(i, color)
        for i in old_word_leds:
            ctrl.set_pixel(i)
        ctrl.show_pixels()
        time.sleep(0.01)

    # Fade old words out
    if set(old_word_leds).issubset(set(new_word_leds)) == False:
        for j in range(128):
            ctrl.clear_pixels()
            for i in old_word_leds:
                color = get_color(ctrl.color, (1 - j / 128))
                ctrl.set_pixel(i, color)
            for i in new_word_leds:
                ctrl.set_pixel(i)
            ctrl.show_pixels()
            time.sleep(0.01)

    ctrl.set_pixels(new_word_leds)

def get_color(color, percent):
    r = color[0]
    g = color[1]
    b = color[2]

    r = int(max(0, r * percent))
    g = int(max(0, g * percent))
    b = int(max(0, b * percent))

    color = np.array([r, g, b])
    return color
