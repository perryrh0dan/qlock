from opt3001 import opt3001


class Controller():
    def __init__(self, address, bus):
        self.opt = opt3001.OPT3001(address, bus)
        self.opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)


    def get_brightness(self):
        return self.opt.read_lux_float()
