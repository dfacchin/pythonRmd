"""
End-effector trajetory (x,y) for the PICKING task
Given some Path_points = [[x1,y1],[x2,y2],...[xn,yn]]
It generates Traj_points = []
"""
import numpy as np
from shapely.geometry import LineString

class TrajectoryPlanner:

    def __init__(self, path_points, linear_steps=2, parabola_steps=20):

        self.pp = path_points
        self.l_steps = linear_steps
        self.p_steps = parabola_steps

        # beta is the internal angle associated to each path point
        # (between two linear paths)
        self.beta_angles = [] # [rad]
        self.beta_max = 3  #(5/6)*np.pi
        self.beta_min = 0.02 #np.pi/8

        self.L = [] # [mm]
        self.L_max = 80
        self.L_min = 10

        # Parabola start and end points
        self.p_start = []
        self.p_end = []

        # Linear start and end points
        self.lin_start = []
        self.lin_end = []

        # New reference system [sev = start,end,vertex]
        self.Xp_sev = []
        self.Yp_sev = []

        # New reference system parabola trajectory points
        self.Xp_traj = []
        self.Yp_traj = []

        # Coordinates of all the points of the end-effector trajectory
        self.eef_traj_x = []
        self.eef_traj_y = []

        # Split the trajectory in points that are equally spaced
        self.distance_delta = 30 # [mm]

        # Coordinates of equally spaced trajectory points 
        self.equal_traj_x = []
        self.equal_traj_y = []
        self.equal_traj_xy = []



    def parabolic_path(self):
        """
        Main method in which the entire end-effector trajectory is generated
        """
        if len(self.pp) == 1:
            # TODO raise an error
            pass

        elif len(self.pp) == 2:
            # Linear line (no parabola needed for only two path points)
            self.linear_path(self.pp[0][0],self.pp[0][1],self.pp[1][0],self.pp[1][1])

        else:
            self.internal_angles() # beta [rad]
            self.L_line() # L [mm]
            self.parabola_extremity() # p_start, p_end
            self.linear_extremity() # lin_start, lin_end

            for idx in range(len(self.pp)):
                if idx+1 < len(self.pp):
            
                    # FIRST line
                    if idx == 0:
                        print("beta list: ", self.beta_angles)

                        # Linear line
                        self.linear_path(self.lin_start[idx][0],self.lin_start[idx][1],self.lin_end[idx][0],self.lin_end[idx][1])

                        if (self.beta_max > self.beta_angles[idx+1] > self.beta_min):
                            # Parabola axis
                            self.parabola_axis_vertex(self.pp[idx+1][0],self.pp[idx+1][1],self.p_start[idx][0],self.p_start[idx][1],self.p_end[idx][0],self.p_end[idx][1])
                            # Generate parabola
                            self.generate_parabola(idx)

                    # LAST line
                    elif idx == len(self.pp)-2:
                        # Linear line
                        self.linear_path(self.lin_start[idx][0],self.lin_start[idx][1],self.lin_end[idx][0],self.lin_end[idx][1])
                    
                    # MID lines
                    else:
                        # Linear line
                        self.linear_path(self.lin_start[idx][0],self.lin_start[idx][1],self.lin_end[idx][0],self.lin_end[idx][1])

                        if (self.beta_max > self.beta_angles[idx+1] > self.beta_min):
                            # Parabola axis
                            self.parabola_axis_vertex(self.pp[idx+1][0],self.pp[idx+1][1],self.p_start[idx][0],self.p_start[idx][1],self.p_end[idx][0],self.p_end[idx][1])
                            # Generate parabola
                            self.generate_parabola(idx)


    def linear_extremity(self):
        """
        Define start and end points (x,y) of the linear paths
        """
        for idx in range(len(self.pp)):
            if idx+1 < len(self.pp):

                if idx == 0:
                    # First line START point
                    self.lin_start.append([self.pp[idx][0], self.pp[idx][1]])
                    # First line END point
                    if (self.beta_max > self.beta_angles[idx+1] > self.beta_min):
                        self.lin_end.append([self.p_start[idx][0], self.p_start[idx][1]])
                    else:
                        self.lin_end.append([self.pp[idx+1][0], self.pp[idx+1][1]])

                elif idx == len(self.pp)-2:
                    # Last line START point
                    if (self.beta_max > self.beta_angles[idx] > self.beta_min):
                        self.lin_start.append([self.p_end[idx-1][0], self.p_end[idx-1][1]])
                    else:
                        self.lin_start.append([self.pp[idx][0], self.pp[idx][1]])
                    # Last line END point
                    self.lin_end.append([self.pp[idx+1][0], self.pp[idx+1][1]])

                else:
                    # Mid lines START points
                    if (self.beta_max > self.beta_angles[idx] > self.beta_min):
                        self.lin_start.append([self.p_end[idx-1][0], self.p_end[idx-1][1]])
                    else:
                        self.lin_start.append([self.pp[idx][0], self.pp[idx][1]])
                    # Mid lines END points
                    if (self.beta_max > self.beta_angles[idx+1] > self.beta_min):
                        self.lin_end.append([self.p_start[idx][0], self.p_start[idx][1]])
                    else:
                        self.lin_end.append([self.pp[idx+1][0], self.pp[idx+1][1]])


    def generate_parabola(self,idx):
        """
        Generate parabolic trajectory
        """
        # Parabola START point
        self.rs_trans(self.p_start[idx][0],self.p_start[idx][1])
        # Parabola END point
        self.rs_trans(self.p_end[idx][0],self.p_end[idx][1])
        # Parabola VERTEX
        self.rs_trans(self.xp_vertex,self.yp_vertex)

        # Parabola intermediate points in the rotated reference system
        self.get_parabola_XY_steps()

        # Inverse rotation to go back to the original reference system
        self.rs_inverse_trans(self.Xp_traj,self.Yp_traj)

        # Empty the lists
        self.empty_lists()


    def internal_angles(self):
        """
        Internal angles (beta) between two linear paths.
        Each angle corresponds to a path point.
        """
        for idx in range(len(self.pp)):
            # No beta angle is needed for trajectory starting and ending points
            if idx == 0 or idx == len(self.pp)-1:
                self.beta_angles.append(None)
            else:
                # Define three points
                prev_pp = self.pp[idx-1]
                curr_pp = self.pp[idx]
                next_pp = self.pp[idx+1]

                # Theorem of the cosine
                l1sq = (prev_pp[0]-curr_pp[0])**2 + (prev_pp[1]-curr_pp[1])**2
                l2sq = (curr_pp[0]-next_pp[0])**2 + (curr_pp[1]-next_pp[1])**2
                l3sq = (next_pp[0]-prev_pp[0])**2 + (next_pp[1]-prev_pp[1])**2
                beta = np.arccos((l1sq+l2sq-l3sq) / (2*np.sqrt(l1sq)*np.sqrt(l2sq)))
                print("beta: ", np.rad2deg(beta))
                self.beta_angles.append(beta)


    def L_line(self):
        """
        Line that goes from the path_point to the start/end point of the parabola.
        L is a linear function of beta
        """
        # Angular coefficient (slope)
        M = (self.L_min - self.L_max) / (self.beta_max - self.beta_min)
        # Height at which the line crosses the y-axis
        Q = (-self.beta_min*((self.L_min-self.L_max) / (self.beta_max-self.beta_min)) + self.L_max)

        for x in self.beta_angles:
            if x != None:
                # Equation of a straight line (y = x*m + q)
                L = x*M + Q
                self.L.append(L)

        print("L: ", self.L)


    def parabola_extremity(self):
        """
        Method to generate start and end points of the parabolic paths.

        :param pp (list): path points
        :param L (list): L_lines
        """
        for idx, pp in enumerate(self.pp):
            if idx != 0 and idx+1 < len(self.pp):
                x1 = self.pp[idx-1][0]
                y1 = self.pp[idx-1][1]
                x2 = self.pp[idx][0]
                y2 = self.pp[idx][1]
                x3 = self.pp[idx+1][0]
                y3 = self.pp[idx+1][1]

                self.get_parabola_xy(self.L[idx-1],x1,y1,x2,y2,x3,y3,start_end=0)
                print("L start: ", self.L[idx-1])
                self.get_parabola_xy(self.L[idx-1],x1,y1,x2,y2,x3,y3,start_end=1)
                print("L end: ", self.L[idx-1])


    def get_parabola_xy(self,L,x_prev,y_prev,x_curr,y_curr,x_next,y_next,start_end=0):
        """
        Calculations to obtain x,y coordinates of start & end parabola points
        """
        print("\n")
        print("xy prev,curr,next: ",x_prev,y_prev,x_curr,y_curr,x_next,y_next)

        if start_end==0:
            # Angular coefficient (slope)
            # m = (y2 - y1) / (x2 - x1)
            y1 = (y_curr - y_prev)
            x1 = (x_curr - x_prev)
            print(f"angular coeff m=y/x  x1: {x1}, y1: {y1}")
            # Slope of the linear line wrt the x-axis
            alpha1 = np.arctan2(y1,x1)
            print("alpha1: ", np.rad2deg(alpha1), "[deg]")

            # Coordinates of the parabola START point
            xp = x_curr - L*np.cos(alpha1)
            yp = y_curr - L*np.sin(alpha1)
            print(f"x_start: {xp}, y_start: {yp}")
            self.p_start.append([xp,yp])

        elif start_end==1:
            y2 = (y_next - y_curr)
            x2 = (x_next - x_curr)
            print(f"angular coeff m=y/x  x2: {x2}, y2: {y2}")
            alpha2 = np.arctan2(y2,x2)
            print("alpha2: ", np.rad2deg(alpha2), "[deg]")

            # Coordinates of the parabola END point
            xp = x_curr + L*np.cos(alpha2)
            yp = y_curr + L*np.sin(alpha2)
            print(f"x_end: {xp}, y_end: {yp}")
            self.p_end.append([xp,yp])


    def linear_path(self, x1, y1, x2, y2):
        '''
        Linear End-effector Path Planning:
        Calculates the vector passing through a 'start' and an 'end' point.
        Splits the vector in multiple points that define the path to follow.

        :params x1,y1:   cartesian coordinates of the line start point
        :params x2,y2:   cartesian coordinates of the line end point
        :param steps:    amount of points on the linear vector
                         (start and end points included)

        :return (lists):  [x],[y] coordinates of the points on the vector (steps)
        '''
        steps_x = np.linspace(x1, x2, self.l_steps, endpoint=True)  # (start, stop, steps)
        steps_y = np.linspace(y1, y2, self.l_steps, endpoint=True)

        if x1 == x2:
            for y in steps_y:
                x = x1
                self.eef_traj_x.append(x)
                self.eef_traj_y.append(y)

        elif y1 == y2:
            for x in steps_x:
                y = y1
                self.eef_traj_x.append(x)
                self.eef_traj_y.append(y)

        else:
            for x in steps_x:
                y = (((x-x1)/(x2-x1))*(y2-y1))+y1
                self.eef_traj_x.append(x)
                self.eef_traj_y.append(y)


    def parabola_axis_vertex(self, x_edge, y_edge, xp_s, yp_s, xp_e, yp_e):
        """
        Method to calculate both the parabola axis and its vertex.

        Equation of the parabola axis
        y=m*x+q

        :params x,y edge: coordinates of the path_point.
                          Where a linear path end the next one begins.
        :params xp_s,yp_s,xp_e,yp_e: coordinates of the parabola start and end point.
        """
        # Coordinate of a point on the parabola axis
        xp_mid = (xp_s + xp_e) / 2
        yp_mid = (yp_s + yp_e) / 2

        # Parabola axis
        m = (yp_mid-y_edge) / (xp_mid-x_edge)
        q = yp_mid - (m*xp_mid)
        theta = np.arctan(m)
        self.theta = np.pi/2 - theta

        # Parabola vertiex
        self.xp_vertex = (xp_mid+x_edge) / 2
        self.yp_vertex = (yp_mid+y_edge) / 2

        print("xp_vertex: ", self.xp_vertex)
        print("yp_vertex: ", self.yp_vertex)


    def rs_trans(self,x,y):
        """
        Transformation to go from the original reference system (x,y)
        to the new one (X,Y)
        This transformation is used for the parabola starting and ending point

        :params x,y [mm] (float): cartesian coordinates of start or end parabola points

        :return (float): X and Y coordinates of the start or end point
                         of the parabola wrt new reference system
        """
        # Rotation matrix (counterclockwise)
        R = np.array([[np.cos(self.theta), -np.sin(self.theta)],
                    [np.sin(self.theta), np.cos(self.theta)]])

        # Original reference system
        xy = np.array([[x],
                       [y]])

        # # Original translation
        # q = np.array([[qx],[self.qy]])
        # XY = np.matmul(R,xy) + q

        # New parabola reference system
        XY = np.matmul(R,xy)

        # sev = start, end, vertex
        self.Xp_sev.append(float(XY[0]))
        self.Yp_sev.append(float(XY[1]))
        

    def get_parabola_XY_steps(self):
        """
        Get all the parabola intermediate X,Y points in the new reference system
        """
        A = np.array([[self.Xp_sev[0]**2, self.Xp_sev[0], 1],    # start
                        [self.Xp_sev[1]**2, self.Xp_sev[1], 1],    # end
                        [self.Xp_sev[2]**2, self.Xp_sev[2], 1]])   # vertex

        B = np.array([[self.Yp_sev[0]],    # start
                        [self.Yp_sev[1]],    # end
                        [self.Yp_sev[2]]])   # vertex

        a, b, c = np.linalg.solve(A, B)

        steps_Xp = np.linspace(self.Xp_sev[0], self.Xp_sev[1], self.p_steps, endpoint=False)[1:] #remove the first element by indexing

        for Xp in steps_Xp:
            # Equation of a parabola (quadratic equation)
            Yp = a*Xp**2 + b*Xp + c
            Yp = float(Yp)
            self.Xp_traj.append(Xp)
            self.Yp_traj.append(Yp)

        # Empty lists for the next parabola (start,end,vector)
        self.Xp_sev = []
        self.Yp_sev = []


    def rs_inverse_trans(self,X,Y):
        """
        Inverse transformation to go from the new (rotated) reference system (X,Y)
        to the original one (x,y)
        """
        # Rotation matrix (counterclockwise)
        A = np.array([[np.cos(self.theta), -np.sin(self.theta)],
                    [np.sin(self.theta), np.cos(self.theta)]])
        
        for Xi,Yi in zip(X,Y):
            
            B = np.array([[Xi],
                          [Yi]])
            
            x, y = np.linalg.solve(A, B)

            self.eef_traj_x.append(float(x))
            self.eef_traj_y.append(float(y))


    def empty_lists(self):
        """
        Empty lists to populate them with new
        trajectory values
        """
        self.L_line = []
        self.X = []
        self.Y = []
        self.Xp_sev = []
        self.Yp_sev = []
        self.Xp_traj = []
        self.Yp_traj = []


    def equally_spaced_lines(self):
        """
        Split the entire trajectory in equally spaced straight lines
        Reminder: to access elements of shapely.geometry.LineStrig (python module),
                  you have to use .coords
        """
        trajectory_points = []

        for x,y in zip(self.eef_traj_x,self.eef_traj_y):
            trajectory_points.append([x,y])

        # Create a line connecting all the points
        line = LineString(trajectory_points)

        # Return evenly spaced values within a given interval
        distances = np.arange(0, line.length, self.distance_delta)
        #print("distances: ", distances)

        # NOTE: the last point is added with (+ [line.coords[-1]).
        #       This point may not be equally spaced as the previous ones.
        points = [line.interpolate(distance) for distance in distances] + [line.coords[-1]]

        # New line with equally spaced points
        new_line = LineString(points)

        for x,y in new_line.coords[:]:
            self.equal_traj_x.append(x)
            self.equal_traj_y.append(y)
            self.equal_traj_xy.append([x,y])


if __name__ == "__main__":

    #Points = [[0,0],[0,200],[0,400],[200,400],[500,400],[800,400],[400,405]]
    #Points = [[0,200], [-300,400], [0,502],[300,600], [0,600], [0,800], [0,1000], [0,1200]]
    #Points = [[0,200], [-300,400],[300,600], [0,600], [0,800]]
    #Points = [[0,200], [-300,400], [300,600], [0,800], [0,1000], [0,1200], [0,1500]]
    #Points = [[0,200], [0,400], [150,400], [300,400], [300,100], [800, 600], [0, 1000], [500, 1000]]
    #Points = [[0,200], [0,400], [300,400], [300,-300],[-300,-400], [0, 1000], [500, 1000],[0,200], [-300,400], [300,600]]
    Points = [[0,0],[-400,400],[0,600]]
    #Points = [[0,0],[500,800]]


    # Generate the trajectory
    traj1 = TrajectoryPlanner(Points)
    traj1.parabolic_path()
  
    # Generate equally spaced lines
    traj1.equally_spaced_lines()

    # Plot
    import matplotlib.pyplot as plt
    
    # path points
    for pp in traj1.pp:
        plt.plot(pp[0],pp[1], marker=(5,0), label="pp")

    # # parabola start
    # for s in traj1.p_start:
    #     plt.plot(s[0],s[1], marker=".", label="p_start")

    # # parabola end
    # for e in traj1.p_end:
    #     plt.plot(e[0],e[1], marker=(5,2), label="p_end")

    # parabola vertex
    #plt.plot(, marker=(5,2), label="p_vertex")


    plt.plot(traj1.equal_traj_x, traj1.equal_traj_y, marker=(5,2), label="lin")

    # Set equal axis aspect
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()