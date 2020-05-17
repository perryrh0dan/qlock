import RPi.GPIO as GPIO

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Controller():
    def __init__(self):
        self.PIXEL_COUNT = 114

        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        self.pixel = Adafruit_WS2801.WS2801Pixels(
            self.PIXEL_COUNT, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE), gpio=GPIO)

        self.color = [255, 255, 255]
        self.brightness = 1
        self.pixel.clear()
        self.pixel.show()

    def change_color(self, color):
        self.color = color

    def change_brightness(self, brightness):
        self.brightness = abs(brightness / 100)

    def turn_on(self, leds, colors = []):
        self.pixel.clear()
        if len(colors) > 0
            for led in leds:
                self.set_pixel(led, self.color)
        else:
            for i, led in enumerate(leds):
                self.set_pixel(led, colors[i])


    def set_pixel(self, led, color):
        color = Adafruit_WS2801.RGB_to_color(
            color[0] * self.brightness, color[1] * self.brightness, color[2] * self.brightness)
        self.pixel.set_pixel(led, color)

    def turn_off(self):
        self.pixel.clear()
        self.pixel.show()
