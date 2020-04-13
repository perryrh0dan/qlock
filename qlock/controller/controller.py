import RPi.GPIO as GPIO

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Controller():
    def __init__(self):
        self.PIXEL_COUNT = 114

        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        self.pixel = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE), gpio=GPIO)

        self.color = [255, 255, 255]
        self.pixel.clear()
        self.pixel.show()
        self.on = False

    def change_color(self, color):
        self.color = color

    def turn_on(self, leds):
        self.pixel.clear()
        for led in leds:
            self.pixel.set_pixel(led, Adafruit_WS2801.RGB_to_color(self.color[0], self.color[1], self.color[2]))
        self.pixel.show()
        self.on = True

    def turn_off(self):
        self.pixel.clear()
        self.pixel.show()
        self.on = False