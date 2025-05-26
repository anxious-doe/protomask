import time
from pimoroni_i2c import PimoroniI2C
from breakout_matrix11x7 import BreakoutMatrix11x7
from largeanim import anim_happy_blink

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**PINS_PICO_EXPLORER)

MATRIX1 = BreakoutMatrix11x7(i2c, address=0x77)
MATRIX2 = BreakoutMatrix11x7(i2c, address=0x75)

print('running')

x = 0
y = 0
light = True

ANIM_DELAY = 0.03
FRAMESIZE = (11, 14)
BRIGHTNESS = 64

def render_frame(frame: list, framesize: tuple, matrix1, matrix2, brightness: int):
    
    #print(f"frame len: {len(frame)}")
    rows = framesize[0]
    cols = framesize[1]
    single_display_cols = int(cols/2)
    #print(f"rows: {rows}")
    #print(f"cols: {cols}")
    
    for row in range(0, rows):
        #print(f"row {row}")
        for col in range(0, cols):
            #print(f"col {col}")
            pixel_val = frame[row][col]
            
            if col < cols/2:
                adjusted_col = single_display_cols - 1 - col
                #print(f"matrix1: col: {col} adjusted col: {adjusted_col}")
                matrix1.set_pixel(row, adjusted_col, pixel_val * brightness)
            else:
                adjusted_col = int(col - cols/2)
                adjusted_row = rows - 1 - row
                #print(f" col: {col} adjusted col: {adjusted_col} row: {row} adjusted row: {adjusted_row}")
                matrix2.set_pixel(adjusted_row, adjusted_col, pixel_val * brightness)
    matrix1.update()
    matrix2.update()

def play_anim(anim: list, framesize: tuple, matrix1, matrix2, brightness: int, delay: float):

    for frame_index in range(0, len(anim)):
        print(f'frame index: {frame_index}')
        frame = anim[frame_index]
        render_frame(frame=frame, framesize=framesize, matrix1=matrix1, matrix2=matrix2, brightness=brightness)

        matrix2.update()
        matrix1.update()
            
        time.sleep(delay)

play_anim(anim=anim_happy_blink, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=ANIM_DELAY)


