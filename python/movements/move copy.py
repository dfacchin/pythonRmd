import robot.kinematics as kinematics


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


def pick_move(home, drop, apple_coords, pick_offset, drop_offset, steps=3):
    pp = [] # path points

    for apple_coord in apple_coords:

        x_h = home[0] # x_coord of home_pose
        y_h = home[1] # y_coord of home_pose
        x_a = apple_coord[0] # x_coord of apple
        y_a = apple_coord[1] # y_coord of apple

        # from current eef pose --> to safe zone limit (perpendicular to apple)
        face_apple = kinematics.path(x_h, y_h, x_a-pick_offset, y_a, steps)
        pp.append(face_apple)

        # from safe zone limit --> to apple
        approach_apple = kinematics.path(x_a-pick_offset, y_a, x_a, y_a, steps=3)
        approach_apple.pop(0) # rm the first element of the list
        pp.append(approach_apple)
        print("approach: ", approach_apple)

        # from apple --> back to safe zone limit 
        retract = kinematics.path(x_a, y_a, x_a-pick_offset, y_a, steps=3)
        retract.pop(0) # rm the last element of the list
        print("last retract: ", retract)
        pp.append(retract)
        
        # from safe zone limit --> to via point
        # via points
        left_q = [[400,0]] # for apples in the left quadrant
        right_q = [[350,400]] # for apples in the right quadrant

        if retract[1][1] <= 0:
            pp.append(left_q)
        else:
            pp.append(right_q)

        # from via point --> to drop offset
        x_d = drop[0]
        y_d = drop[1]
        approach_drop = [drop[0]+drop_offset, drop[1]]
        print('approach_drop: ', approach_drop)
        pp.append(approach_drop)

        # from drop offset --> to drop pose
        pp.append(drop)

        list_pp = sum(pp, []) # create one single list
    return list_pp


def spray_move():
    pass

