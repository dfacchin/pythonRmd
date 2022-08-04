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


def pick_move(home, eef_pose, apple_pose, linear_limit, pre_drop, drop):

    # get current eef position [x_eef, y_eef]
    x_eef = eef_pose[0]
    y_eef = eef_pose[1]
    # get desired apple position [x_a, y_a]
    x_a = apple_pose[0]
    y_a = apple_pose[1]

    # define sequences of path points (pp) based on specific cases.
        # the cases depend on: [x_eef, y_eef] and [x_a, y_a]

    

    # pp sequances:
    # - eef current pose --> linear limit
    # - linear limit --> desired apple
    # - desired apple --> linear limit
    # - linear limit --> pre-drop pose
    # - pre-drop pose --> drop pose

    pass


def spray_move():
    pass
