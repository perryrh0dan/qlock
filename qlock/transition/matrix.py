import time
import utils
import numpy as np


def start(ctrl, old_word_leds, new_word_leds):
    direction = 'y'
    length = np.random.randint(5, 13, 11)
    start = list(map(lambda x: -1 * (x + np.random.randint(0, 5)), length))
    max_length = -1 * np.min(start)

    active_old_word_leds = old_word_leds
    active_new_word_leds = []

    for y in range(11 + max_length):
        leds = active_new_word_leds
        for x in range(len(start)):
            start_x = x
            start_y = start[x] + y + 1
            strip_length = length[x]

            leds = leds + \
                utils.get_leds_xy(start_x, start_y, strip_length, direction)

        active_new_word_leds = list(set(leds).intersection(new_word_leds))
        active_old_word_leds = [
            x for x in active_old_word_leds if x not in leds]
        leds += active_old_word_leds

        leds = list(dict.fromkeys(leds))
        blocked_indices = get_indices(leds, active_new_word_leds)
        colors = get_color_values(ctrl.color, len(leds), blocked_indices)
        ctrl.set_pixels(leds, colors)
        time.sleep(0.05)


def get_color_values(default, n, blocked_indices):
    colors = np.tile(np.array(default), (n, 1))
    for i in range(len(colors)):
        if i in blocked_indices:
            continue
        random1 = np.random.random_sample()
        if random1 < 0.6:
            continue
        random2 = np.random.random_sample()
        colors[i] = get_color(colors[i], random2)
    return colors

def get_color(color, saturation):
    color = np.array(color)
    white = np.array([255,255,255])
    vector = white - color
    return color + vector * saturation


def get_indices(full, part):
    n = []
    for i in range(len(full)):
        if full[i] in part:
            n.append(i)
    return n
