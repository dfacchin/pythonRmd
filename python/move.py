import kinematics

'''
These functions store a set of predefined path point that we want the eef
always to pass throgh when executing picking/spraying procedure.
'''

# Predefined positions
home = [300,0]
drop = [-200,400]
apple = [700,200]
depth_offset = 0 # [mm]

def pick_move(apple_coords):
    pp = [] # path points

    x_h = home[0] # x_coord of home_pose
    y_h = home[1] # y_coord of home_pose
    x_a = apple_coords[0][0] # x_coord of apple
    y_a = apple_coords[0][1] # y_coord of apple

    # eef path points form 'home' until the pose in front of the apple
    # with a distance equal to the depth_offset 
    face_apple = kinematics.path(x_h, y_h, x_a, y_a, steps=3)
    pp.append(face_apple)

    pp.append(drop)
    pp.append(home)

    pass

def spray_move():
    pass

