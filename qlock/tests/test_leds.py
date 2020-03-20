# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 32
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
 
 
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0.1):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(pixels, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.02)
            
 
if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!
 
    rainbow_cycle_successive(pixels, wait=0.1)
    rainbow_cycle(pixels, wait=0.01)
 
    brightness_decrease(pixels)
    
    appear_from_back(pixels)
    
    for i in range(3):
        blink_color(pixels, blink_times = 1, color=(255, 0, 0))
        blink_color(pixels, blink_times = 1, color=(0, 255, 0))
        blink_color(pixels, blink_times = 1, color=(0, 0, 255))
 
    
    
    rainbow_colors(pixels)
    
    brightness_decrease(pixels)