import numpy as np
import move


# Predefined positions
home = [300,0]
drop = [[-200,400]]
pick_offset = 200 # [mm]
drop_offset = 200 # [mm]
apple_coords = [[700,-200],[700,200],[800,300],[650,350]]

path = move.pick_move(home, drop, apple_coords, pick_offset, drop_offset)
print("path: ", path)
