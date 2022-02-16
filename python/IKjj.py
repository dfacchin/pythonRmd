# Resolve the Inverse Kinematics of the robot (x,y) => Angle1, Angle2
#  x,y in milimetes (mm). Return angle A1, A2 in degrees.
#  there are two posible solutions (depends on elbow configuration)

#LEN1 =497
#LEN2 =500


def IK(self,x=0,y=0,elbow=0,verbose=False):
	len1 = 497
	len2 = 500
	if (elbow==1):  # inverse elbow solution: reverse X axis, and final angles.
		x = -x;
	dist = math.sqrt(x*x+y*y);  # distance
	if (dist > (len1+len2)):
		dist = (len1+len2)-0.001;
		if (verbose):
			print("IK overflow->limit");
	D1 = math.atan2(y,x);
	# Law of cosines (a,b,c) = acos((a*a+b*b-c*c)/(2*a*b))
	D2 = math.acos((dist*dist + len1*len1 - len2*len2) / (2.0 * dist*len1))
	A1 = math.degrees(D1+D2)-90 # Our robot configuration
	A2 = math.acos((len1*len1 + len2*len2 - dist*dist) / (2.0 * len1*len2))
	A2 = math.degrees(A2) - 180    # Our robot configuration
	if (elbow==1):
		A1 = -A1
		A2 = -A2
	if (verbose):
		print("IK xy:",x,y,"elbow:",elbow," A1A2:",A1,A2)
	return A1,A2
	
inverse = IK(x=400, y=0, elbow=0, verbose=False)
print(inverse)
