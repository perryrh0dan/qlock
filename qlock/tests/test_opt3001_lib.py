import time
from opt3001 import opt3001

address = 0x44

opt = opt3001.OPT3001(address)

opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)

while(True):
    print(opt.read_lux_float())
    time.sleep(1)