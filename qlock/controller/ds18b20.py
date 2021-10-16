# Temperature Sensor
class Controller():
    def __init__(self, device_dir):
        self.device_dir = device_dir
        self.device = device_dir + "/w1_slave" 

    def read_temp_raw(self):
        f = open(self.file_dir, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_temp(self):
        lines = self.read_temp_raw()
        line = lines[1]
        index = line.find("t=")
        temp_raw = line[index+2:]
        temp = round(float(temp_raw) / 1000)
        return temp
