import kinematics


'''
These functions store a set of predefined path point that we want the eef
always to pass throgh when executing picking/spraying procedure.
'''

# Predefined Path Points
home = [250,0]
drop = [-500,500]
Bm = [425,0]
Br = [250,500]
Bl = [250,-500]

# Define a limit within we can move freely
x_lim = 600
y_lim = None # range(1000,-1000)
linear_limit = [x_lim, y_lim]


def pick_move(home, eef_pose, apple_pose, safezone_limit, pre_drop, drop, steps):

    # Get current eef position [x_eef, y_eef]
    x_eef = eef_pose[0]
    y_eef = eef_pose[1]
    # Get desired apple position [x_a, y_a]
    x_a = apple_pose[0]
    y_a = apple_pose[1]

    # Define the safe-zone limit (eef within safe-zone perpendicular to apple)
    x_sz = 600
    y_sz = apple_pose[1]

    # Define sequences of path points (pp) based on specific cases
    pp = []

    # Apple on the RIGHT side
    if y_a > 0:
        
        # Eef on the RIGHT side
        if (0 <= x_eef <= x_sz) and (0 <= y_eef < 1000):
            # Go straight to the safezone_limit
            face_apple = kinematics.linear_path(x_eef, y_eef, x_sz, y_sz, steps)
            pp.append(face_apple)

        # Eef on the LEFT side
        elif (250 <= x_eef <= x_sz) and (0 >= y_eef > -1000):
            # Go straight to the safezone_limit
            face_apple = kinematics.linear_path(x_eef, y_eef, x_sz, y_sz, steps)
            pp.append(face_apple)

        else:
            print("End-effector is in a non defined position!")

    # Apple on the LEFT side
    if y_a < 0:

        # Eef on the LEFT side
        if (0 <= x_eef <= x_sz) and (0 >= y_eef > -1000):
            # Go straight to the safezone_limit
            face_apple = kinematics.linear_path(x_eef, y_eef, x_sz, y_sz, steps)
            pp.append(face_apple)

        # Eef on the RIGHT side
        if (y_a < 0) and (250 <= x_eef <= x_sz) and (0 <= y_eef < 1000):
            # Go straight to the safezone_limit
            face_apple = kinematics.linear_path(x_eef, y_eef, x_sz, y_sz, steps)
            pp.append(face_apple)
        
        else:
            print("End-effector is in a non defined position!")



    # pp sequances:
    # - eef current pose --> linear limit
    # - linear limit --> desired apple
    # - desired apple --> linear limit
    # - linear limit --> pre-drop pose
    # - pre-drop pose --> drop pose

    pass


def spray_move():
    pass
