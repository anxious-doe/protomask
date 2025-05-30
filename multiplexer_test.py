from machine import I2C, Pin
from pimoroni_i2c import PimoroniI2C
from breakout_matrix11x7 import BreakoutMatrix11x7


# Direct I2C bus for unique address devices
i2c = PimoroniI2C(sda=20, scl=21)

# Multiplexer select function
def select_mux_channel(i2c, channel):
    if 0 <= channel <= 3:
        i2c.writeto(0x70, bytes([1 << channel]))

# For matrixes behind the multiplexer:
def get_mux_matrix(channel, address):
    select_mux_channel(i2c, channel)
    return BreakoutMatrix11x7(i2c, address=address)

select_mux_channel(i2c, 0)
MATRIX1 = BreakoutMatrix11x7(i2c, address=0x75)
MATRIX2 = BreakoutMatrix11x7(i2c, address=0x77)

select_mux_channel(i2c, 1)
MATRIX3 = get_mux_matrix(0, 0x75)
MATRIX4 = get_mux_matrix(1, 0x77)

# ----

select_mux_channel(i2c, 0)
MATRIX1.set_pixel(0, 0, 100)
MATRIX2.set_pixel(0, 1, 100)
MATRIX1.update()
MATRIX2.update()

select_mux_channel(i2c, 1)
MATRIX3.set_pixel(0, 2, 100)
MATRIX4.set_pixel(0, 3, 100)
MATRIX3.update()
MATRIX4.update()
