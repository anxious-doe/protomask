import time
from pimoroni_i2c import PimoroniI2C
from breakout_matrix11x7 import BreakoutMatrix11x7

from anim_square import anim_square
from anim_cross import anim_cross
from anim_heart import anim_heart
from anim_question import anim_question
from anim_exclamation import anim_exclamation
from anim_chevron_side import anim_chevron_side, anim_chevron_side_blink, anim_chevron_side_to_up
from anim_chevron_up import anim_chevron_up, anim_chevron_up_blink, anim_chevron_up_to_side

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**PINS_PICO_EXPLORER)

MATRIX1 = BreakoutMatrix11x7(i2c, address=0x75)
MATRIX2 = BreakoutMatrix11x7(i2c, address=0x77)

print('running')

x = 0
y = 0
light = True

ANIM_DELAY = 0.4
FRAMESIZE = (11, 14)
BRIGHTNESS = 60

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
        #print(f'frame index: {frame_index}')
        frame = anim[frame_index]
        render_frame(frame=frame, framesize=framesize, matrix1=matrix1, matrix2=matrix2, brightness=brightness)

        matrix2.update()
        matrix1.update()
            
        time.sleep(delay)

DELAY_BETWEEN_ANIMS = 1.5
while True:
    play_anim(anim=anim_chevron_up, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=1)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_chevron_up_blink, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.1)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_chevron_up_to_side, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.2)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_chevron_side_blink, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.1)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_chevron_side_to_up, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.2)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_exclamation, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.2)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_question, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.2)
    time.sleep(DELAY_BETWEEN_ANIMS)
    play_anim(anim=anim_heart, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.2)
    time.sleep(DELAY_BETWEEN_ANIMS)
    for i in range(5):
        play_anim(anim=anim_cross, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.4)
    time.sleep(DELAY_BETWEEN_ANIMS)
    while True:
        play_anim(anim=anim_square, framesize=FRAMESIZE, matrix1=MATRIX1, matrix2=MATRIX2, brightness=BRIGHTNESS, delay=0.1)
    











