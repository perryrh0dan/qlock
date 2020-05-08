#!/usr/bin/python
import smbus
import time

bus = smbus.SMBus(1)

# I2C-Adresse des MCP23017
address = 0x44

# Constants
I2C_LS_REG_CONFIG = 0x01
I2C_LS_REG_RESULT = 0x00

I2C_LS_CONFIG_CONT_FULL_800MS = 0xcc10 # Configdata for Register "Configuration"
                                       # Bit 15..12 Automatic Full-Scale Setting Mode Bit 11 Conversion timefield: 800ms# Erzeugen einer I2C-Instanz und Öffnen des Busses Bit
                                       # 10..9 Mode of conversion: Continuous conversionsbus = smbus.SMBus(1)
                                       # Bit 4 Latch fieldtime.sleep(1)

def read_register(adr):
    return bus.read_byte_data(address, adr)

def read_register_16bit(adr):
    a1 = (adr >> 8) & 0xFF
    a0 = adr & 0xFF
    bus.write_i2c_block_data(address, a1, [a0])
    data0 = bus.read_byte(address)
    data1 = bus.read_byte(address)
    return (data0 << 8) | (data1 & 0xFF)

def write_register(adr, data):
    return bus.write_byte_data(address, adr, data)

def write_register_16bit(adr, data):
    d1 = (data >> 8) & 0xFF
    d0 = data & 0xFF
    return bus.write_i2c_block_data(address, adr, [d1, d0])

def write_config_reg(data):
    return write_register_16bit(I2C_LS_REG_CONFIG, data)

def read_lux_fixpoint():
    # Register Value
    req_value = read_register_16bit(I2C_LS_REG_RESULT)
 
    # Convert to LUX
    mantisse = req_value & 0x0fff
    exponent = req_value & 0xf000 >> 12;

    return 2**exponent * mantisse * 0.01 # mantisse << exponent * 0.01;

# Konfiguration des Opt3001
# Lese Manufacturer ID vom Lichtsensor
print(read_register(0x7E))

# Initialisierung im Continouous Mode
write_config_reg(I2C_LS_CONFIG_CONT_FULL_800MS)

while True:
  # Read I2C-LS
  print(read_lux_fixpoint())
  time.sleep(1)