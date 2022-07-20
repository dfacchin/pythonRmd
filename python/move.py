import kinematics


'''
These functions store a set of predefined path point that we want the eef
always to pass throgh when executing picking/spraying procedure.
'''


def pick_move(home, drop, apple_coords, depth_offset, steps=3):
    pp = [] # path points

    for apple_coord in apple_coords:

        x_h = home[0] # x_coord of home_pose
        y_h = home[1] # y_coord of home_pose
        x_a = apple_coord[0] # x_coord of apple
        y_a = apple_coord[1] # y_coord of apple

        # eef path points form 'home' until the pose in front of the apple
        # with a distance equal to the depth_offset 
        face_apple = kinematics.path(x_h, y_h, x_a-depth_offset, y_a, steps)
        pp.append(face_apple)

        # pp from the depth_offset to the apple
        approach_apple = kinematics.path(x_a-depth_offset, y_a, x_a, y_a, steps=3)
        approach_apple.pop(0) # rm the first element of the list
        pp.append(approach_apple)
        print("approach: ", approach_apple)

        approach_apple.reverse()
        print("retract: ", approach_apple)
        approach_apple.pop() # rm the last element of the list
        pp.append(approach_apple)

        # # pp from the apple pose back to the depth_offset
        # retract = approach_apple
        # retract.reverse()
        # print("retract: ", retract)
        # retract.pop() # rm the last element of the list
        # pp.append(retract)
        
        pp.append(drop)

    return pp


def spray_move():
    pass

