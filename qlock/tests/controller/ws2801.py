class Controller():
    name = 'WS2801'

    def change_color(self, color):
        print(self.name + ' - Change color to: ' + str(color))

    def change_brightness(self, brightness):
        print(self.name + ' - Set brightmess to : ' + str(brightness))

    def turn_on(self, leds, colors = None):
        print(self.name + ' - Turn on leds: ' + str(leds))

    def turn_off(self):
        print(self.name + ' - Turn off leds')
