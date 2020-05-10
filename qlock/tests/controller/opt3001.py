class Controller():
    name = 'OPT3001'

    def __init__(self, address, bus):
        print(self.name + ' - Address: ' + str(hex(address)))
        print(self.name + ' - Bus: ' + str(bus))

    def get_brightness(self):
        return 1500
