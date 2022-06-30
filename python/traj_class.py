import numpy as np

class Joint:

    # Class variables
    time = [0, 2, 4, 8, 10] # [s]
    steps = 6

    def __init__(self, theta, theta_d, v):
        # Define instance variables (unique to each instance)
        self.theta = theta
        self.theta_d = theta_d
        self.v = v

    # Velocity in each segment
    def velocity(self):
        for index, (el_time,el_theta) in enumerate(zip(self.time,self.theta)):
            if (index+1 < len(self.time)): # compute only until the second to last value
                self.v.append((self.theta[index+1]-self.theta[index])/(self.time[index+1]-self.time[index]))
        return self.v

    # Velocity at each (pp) path point
    def theta_d_pp(self):
        for index, elem in enumerate(self.v):
            if (index+1 < len(self.v)):
                if np.sign(self.v[index]) == np.sign(self.v[index+1]):
                    self.theta_d.append((self.v[index]+self.v[index+1])/2)
                elif np.sign(self.v[index]) != np.sign(self.v[index+1]):
                    self.theta_d.append(0)
        self.theta_d.append(0) # this represents the endpoint-velocity (i.c.)
        return self.theta_d

    # Angular displacement and velocity along each trajectory segment (they are a function of time)
    def trajectory(self):
        for index, (el_time,el_theta,el_theta_d) in enumerate(zip(self.time,self.theta,self.theta_d)):
            if (index+1 < len(self.theta)):
                t = np.linspace(self.time[index], self.time[index+1], self.steps) # [s] Time

                # c-coefficients
                c0 = self.theta[index]
                c1 = self.theta_d[index]
                c2 = ((-3*(self.theta[index]-self.theta[index+1])) - (2*self.theta_d[index] + self.theta_d[index+1]) * (self.time[index+1]-self.time[index])) / (self.time[index+1]-self.time[index])**2
                c3 = ((2*(self.theta[index]-self.theta[index+1])) + (self.theta_d[index] + self.theta_d[index+1]) * (self.time[index+1]-self.time[index])) / (self.time[index+1]-self.time[index])**3

                # Cubic Polinomial [Trajectory of angular displacement]
                theta_t = c0 + (c1*(t-self.time[index])) + (c2*(t-self.time[index])**2) + (c3*(t-self.time[index])**3) # [deg]
                # Cubic Polinomial [Trajectory of angular velocity]
                theta_d_t = c1 + (2*c2*(t-self.time[index])) + (3*c3*(t-self.time[index])**2) # [deg/s]

                # Note: the variables that this function returns are arrays
                return theta_t, theta_d_t
                # print("theta_t: " + str(theta_t))
                # print("theta_d_t: " + str(theta_d_t))
