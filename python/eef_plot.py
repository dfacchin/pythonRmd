import matplotlib.pyplot as plt
import kinematics

'''
Plot both the desired and actual trajectory and path points of the robot end-effector.
The plot is represented on the horizontal xy-plane
'''
def xy_traj_pp(theta_S, theta_E, pp, actual_theta_S=None, actual_theta_E=None):
    desired_x = []
    desired_y = []
    actual_x = []
    actual_y = []

    for idx in range(len(theta_S)):
        target = [theta_S[idx], theta_E[idx]] # [theta_S, theta_E]
        xy_coord = kinematics.DK(target)
        desired_x.append(xy_coord[0])
        desired_y.append(xy_coord[1])

    if actual_theta_S != None and actual_theta_E != None:
        for idx in range(len(actual_theta_S)):
            target = [actual_theta_S[idx], actual_theta_E[idx]] # [theta_S, theta_E]
            xy_coord = kinematics.DK(target)
            actual_x.append(xy_coord[0])
            actual_y.append(xy_coord[1])

    plt.title("Path of the end-effector")
    plt.xlabel("x-values")
    plt.ylabel("y-values")
    plt.plot(desired_x, desired_y, color='y', marker='.', label="Desired path")
    if actual_theta_S != None and actual_theta_E != None:
        plt.plot(actual_x, actual_y, marker='.', label="Actual path")

    # Plot desired path points (pp)
    x_pp = []
    y_pp = []

    for i in pp:
        x_pp.append(i[0])
        y_pp.append(i[1])
    plt.scatter(x_pp, y_pp, color='r', marker='o', label="Path points")

    # Define displayed values on axes
    plt.xticks(list(range(0,1100,50)))
    plt.yticks(list(range(-600,600,50)))

    # Invert y-axis
    ax = plt.gca() # get current axis
    ax.invert_yaxis() # revert y-axis

    plt.legend()
    plt.grid(True)

    plt.tight_layout() # avoid text overlapping
    plt.show()
