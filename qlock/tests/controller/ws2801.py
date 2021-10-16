verbose = False

class Controller():
    name = 'WS2801'
    color = [0, 255, 0]

    def __init__(self, pixel_count):
        print(self.name + ' - Pixel Count: ' + str(pixel_count))

    def change_color(self, color):
        print(self.name + ' - Change color to: ' + str(color))

    def change_brightness(self, brightness):
        print(self.name + ' - Set brightmess to : ' + str(brightness))

    def set_pixels(self, leds, colors=[]):
        if verbose:
            print(self.name + ' - Turn on leds: ' + str(leds))

    def set_pixel(self, led, color=[]):
        if verbose:
            print(self.name + ' - Turn on led: ' + str(led))

    def show_pixels(self):
        if verbose:
            print(self.name + ' - Show pixels')

    def clear_pixels(self):
        if verbose:
            print(self.name + ' - Clear pixels')

    def turn_off(self):
        print(self.name + ' - Turn off leds')
