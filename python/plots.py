import matplotlib.pyplot as plt
import kinematics

def path_plot(theta_S, theta_E, actual_theta_S=None, actual_theta_E=None):
    x = []
    y = []

    for idx in range(len(theta_S)):
        target = [theta_S[idx], theta_E[idx]] # [theta_S, theta_E]
        xy_coord = kinematics.DK(target)
        x.append(xy_coord[0])
        y.append(xy_coord[1])

    print("x: ", x)
    print("y: ", y)

    plt.title("Path of the end-effector")
    plt.xlabel("x-values")
    plt.ylabel("y-values")
    plt.plot(x, y, color='y', marker='.', label="Desired path")
    if actual_theta_S != None and actual_theta_E != None:
        plt.plot(actual_theta_S, actual_theta_E, marker='.', label="Actual path")

    plt.xticks(list(range(0,1000,10)))
    plt.yticks(list(range(-500,500,10)))

    plt.legend()
    plt.grid(True)

    plt.tight_layout() # avoid text overlapping
    plt.show()