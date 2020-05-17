import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import numpy as np

PIXEL_COUNT = 114
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(
    PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

pixels.clear()
pixels.show()

leds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
colors = np.tile(np.array([0, 255, 0]), (11, 1))


def set_pixel(led, color):
    adafruit_color = Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2])
    pixels.set_pixel(led, adafruit_color)


def turn_on(leds, colors=[]):
    pixels.clear()
    color = [0, 255, 0]
    if len(colors) <= 0:
        for led in leds:
            set_pixel(led, color)
    else:
        for i, led in enumerate(leds):
            set_pixel(led, colors[i])


if __name__ == "__main__":
    turn_on(leds, colors)



