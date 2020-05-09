from opt3001 import opt3001


class Controller():
    def __init__(self, address, bus):
        opt = opt3001.OPT3001(address, bus)
        opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)
        

    def get_brightness(self):
        return opt.read_lux_float()
