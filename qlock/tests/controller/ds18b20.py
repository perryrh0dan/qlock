class Controller():
    name = 'DS18B20'

    def __init__(self, device_dir):
        self.device_dir = device_dir
        print(self.name + ' - Device Dir: ' + str(device_dir))

    def get_temp(self):
        return 21
