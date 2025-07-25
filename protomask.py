import time
import sys
from pimoroni_i2c import PimoroniI2C
from breakout_matrix11x7 import BreakoutMatrix11x7

from anim_square import anim_square
from anim_cross import anim_cross
from anim_heart import anim_heart
from anim_question import anim_question
from anim_exclamation import anim_exclamation
from anim_chevron_side import anim_chevron_side, anim_chevron_side_blink, anim_chevron_side_to_up
from anim_chevron_up import anim_chevron_up, anim_chevron_up_blink, anim_chevron_up_to_side

I2C = PimoroniI2C(sda=20, scl=21)

def get_mux_matrix(i2c, channel, address):
    """
    Create a matrix object behind the multiplexer.
    
    I don't think that the actual objects matter, so we could possibly only have
    matrix 1 and matrix 2, being 0x77 & 0x75, switching target based on multiplexer
    channel, but this works so I'll keep it for now.
    """
    select_mux_channel(i2c, channel)
    return BreakoutMatrix11x7(i2c, address=address)


def select_mux_channel(i2c, channel):
    """
    Select which channel to output the signals on.
    
    ie if we set channel 0, then all devices wired to multiplexer connections
    sc0, sd0 will see the signal.
    
    So we need to set this before sending commands to each pair of matrixes.
    """
    if 0 <= channel <= 3:
        i2c.writeto(0x70, bytes([1 << channel]))
        
def flip_2d_list(list_2d: list, flip_x: bool = False, flip_y: bool = False):
    flipped_list = list(list_2d)
    if flip_y:
        flipped_list = flipped_list[::-1]
    if flip_x:
        new_flipped_rows = []
        for row in flipped_list:
            new_flipped_rows.append(row[::-1])
        flipped_list = new_flipped_rows
    return flipped_list
        
def render_frame(frame: list, invert_y: bool, framesize: tuple, matrix1, matrix2, brightness: int):
    
    #print(f"frame len: {len(frame)}")
    rows = framesize[0]
    cols = framesize[1]
    single_display_cols = int(cols/2)
    
    frame = flip_2d_list(list_2d=frame, flip_x=False, flip_y=invert_y)
    
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

def play_anim(i2c, eye_positions: dict, eye: str, anim: list, framesize: tuple, matrices: tuple, brightness: int, delay: float):
        
    for frame_index in range(0, len(anim)):
        #print(f"frame {frame_index} / {len(anim)}")

        frame = anim[frame_index]

        if eye == "left" or eye == "both":
            select_mux_channel(i2c, eye_positions["left_channel"])
            matrix1 = matrices[eye_positions["left_left_pos"]]
            matrix2 = matrices[eye_positions["left_right_pos"]]
            invert_y = eye_positions["left_invert_y"]
            render_frame(frame=frame, invert_y=invert_y, framesize=framesize, matrix1=matrix1, matrix2=matrix2, brightness=brightness)
            matrix1.update()
            matrix2.update()
            
        if eye == "right" or eye == "both":
            select_mux_channel(i2c, eye_positions["right_channel"])
            matrix1 = matrices[eye_positions["right_left_pos"]]
            matrix2 = matrices[eye_positions["right_right_pos"]]
            invert_y = eye_positions["right_invert_y"]
            render_frame(frame=frame, invert_y=invert_y, framesize=framesize, matrix1=matrix1, matrix2=matrix2, brightness=brightness)
            matrix1.update()
            matrix2.update()
        
        time.sleep(delay)

print("setting up matrices")
MATRIX0R = get_mux_matrix(I2C, 0, 0x75)
MATRIX0L = get_mux_matrix(I2C, 0, 0x77)

MATRIX1R = get_mux_matrix(I2C, 1, 0x75)
MATRIX1L = get_mux_matrix(I2C, 1, 0x77)

print("initialising variables")

MATRICES = [MATRIX0L, MATRIX0R, MATRIX1L, MATRIX1R]

ANIM_DELAY = 0.4
FRAMESIZE = (11, 14)
BRIGHTNESS = 60

EYE_POSITIONS = {
    "left_channel": 1,
    "right_channel": 0,
    "left_invert_y": False,
    "right_invert_y": True,
    "left_left_pos": 0,
    "left_right_pos": 1,
    "right_left_pos": 2,
    "right_right_pos": 3,
}

print("running")

while True:
    inpt = input(">>>")
    play_anim(i2c=I2C, eye_positions=EYE_POSITIONS, eye="right", anim=anim_chevron_up, framesize=FRAMESIZE, matrices=MATRICES, brightness=100, delay=0.08)
    
    if inpt == "blink":
        print("blinking")
        play_anim(i2c=I2C, eye_positions=EYE_POSITIONS, eye="both", anim=anim_chevron_up_blink, framesize=FRAMESIZE, matrices=MATRICES, brightness=100, delay=0.08)
    elif inpt == "wink":
        play_anim(i2c=I2C, eye_positions=EYE_POSITIONS, eye="left", anim=anim_chevron_up_blink, framesize=FRAMESIZE, matrices=MATRICES, brightness=100, delay=0.08)
    elif inpt == "quit":
        print("quitting")
        sys.exit()
    else:
        print(f"not a command: {inpt}")
