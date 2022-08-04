'''
Trajectory Planning:
Ensure a smooth variation of the joint angles while following a desired path
using the (Cubic) Polinomial Trajectory Function
'''


def cubic_trajectory(time, theta_S, theta_S_d, theta_E, theta_E_d, steps=6):
    # Velocity in each segment
    v_S = [] # Shoulder
    for index, (elem_t,elem_theta_S) in enumerate(zip(time,theta_S)):
        if (index+1 < len(time)): # compute only until the second to last value
            v_S.append((theta_S[index+1]-theta_S[index])/(time[index+1]-time[index]))

    v_E = [] # Elbow
    for index, (elem_t,elem_theta_E) in enumerate(zip(time,theta_E)):
        if (index+1 < len(time)): # compute only until the second to last value
            v_E.append((theta_E[index+1]-theta_E[index])/(time[index+1]-time[index]))

    # Velocity at each path point (Shoulder)
    for index, elem in enumerate(v_S):
        if (index+1 < len(v_S)):
            if np.sign(v_S[index]) == np.sign(v_S[index+1]):
                theta_S_d.append((v_S[index]+v_S[index+1])/2)
            elif np.sign(v_S[index]) != np.sign(v_S[index+1]):
                theta_S_d.append(0)
    theta_S_d.append(0) # this represents the endpoint-velocity (i.c.)

    # Velocity at each path point (Elbow)
    for index, elem in enumerate(v_E):
        if (index+1 < len(v_E)):
            if np.sign(v_E[index]) == np.sign(v_E[index+1]):
                theta_E_d.append((v_E[index]+v_E[index+1])/2)
            elif np.sign(v_E[index]) != np.sign(v_E[index+1]):
                theta_E_d.append(0)
    theta_E_d.append(0) # this represents the endpoint-velocity (i.c.)

    # Solve the Cubic Polinomial for each step:
    # Shoulder
    for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_S,theta_S_d)):
        if (index+1 < len(theta_S)):
            t = np.linspace(time[index], time[index+1], steps) # [s] Time

            # c-coefficients
            c0_S = theta_S[index]
            c1_S = theta_S_d[index]
            c2_S = ((-3*(theta_S[index]-theta_S[index+1])) - (2*theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
            c3_S = ((2*(theta_S[index]-theta_S[index+1])) + (theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

            # Cubic Polinomial [Trajectory of angular displacement]
            theta_S_t = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
            # Cubic Polinomial [Trajectory of angular velocity]
            theta_S_d_t = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

    # Elbow
    for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_E,theta_E_d)):
        if (index+1 < len(theta_E)):
            t = np.linspace(time[index], time[index+1], steps) # [s] Time

            # c-coefficients
            c0_E = theta_E[index]
            c1_E = theta_E_d[index]
            c2_E = ((-3*(theta_E[index]-theta_E[index+1])) - (2*theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
            c3_E = ((2*(theta_E[index]-theta_E[index+1])) + (theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

            # Cubic Polinomial [Trajectory of angular displacement]
            theta_E_t = c0_E + (c1_E*(t-time[index])) + (c2_E*(t-time[index])**2) + (c3_E*(t-time[index])**3) # [deg] Elbow
            # Cubic Polinomial [Trajectory of angular velocity]
            theta_E_d_t = c1_E + (2*c2_E*(t-time[index])) + (3*c3_E*(t-time[index])**2) # [deg/s] Elbow


    # Note: the variables that this function returns are arrays
    return theta_S_t, theta_E_t, theta_S_d_t, theta_E_d_t


def cubic_trajectory_1dof(time, theta, theta_d, steps=6):

    # Velocity in each segment
    v = []
    for index, (elem_t,elem_theta) in enumerate(zip(time,theta)):
        if (index+1 < len(time)): # compute only until the second to last value
            v.append((theta[index+1]-theta[index])/(time[index+1]-time[index]))
    print("v: " + str(v))

    # Velocity at each path point
    for index, elem in enumerate(v):
        if (index+1 < len(v)):
            if np.sign(v[index]) == np.sign(v[index+1]):
                theta_d.append((v[index]+v[index+1])/2)
            elif np.sign(v[index]) != np.sign(v[index+1]):
                theta_d.append(0)
    theta_d.append(0) # this represents the endpoint-velocity (i.c.)
    print("theta_d: " + str(theta_d))

    # Solve the Cubic Polinomial for each step
    for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta,theta_d)):
        if (index+1 < len(theta)):
            t = np.linspace(time[index], time[index+1], steps) # [s] Time

            print("theta[index]: " + str(theta[index]))
            print("theta[index+1]: " + str(theta[index+1]))
            print("theta_d[index]: " + str(theta_d[index]))
            print("theta_d[index+1]: " + str(theta_d[index+1]))

            # c-coefficients
            c0_S = theta[index]
            c1_S = theta_d[index]
            c2_S = ((-3*(theta[index]-theta[index+1])) - (2*theta_d[index] + theta_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
            c3_S = ((2*(theta[index]-theta[index+1])) + (theta_d[index] + theta_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

            print("c0_S: " + str(c0_S))
            print("c1_S: " + str(c1_S))
            print("c2_S: " + str(c2_S))
            print("c3_S: " + str(c3_S))
            # Cubic Polinomial [Trajectory of angular displacement]
            theta_S = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
            # Cubic Polinomial [Trajectory of angular velocity]
            theta_d_S = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

            print("theta_S: " + str(theta_S))
            print("theta_d_S: " + str(theta_d_S))

            # Note: the variables that this function returns are arrays
            #return theta_S, theta_d_S