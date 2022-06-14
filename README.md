# pythonRmd
Python Control for RMD X Motor series

## cmd line
`sudo ip link set can0 type can bitrate 1000000`

`sudo ip link set up can0`

## Scripts
- `Position.py` asks for (x,y) coordinates and the arm reaches them using the inverse kinematics.

- `PosDynDunk.py` executes a picking procedure with all the motors (Gyems, Dynam, Dunker).

- `kinematics.py` contains the function of the inverse kinematics.

- `Calibration.py` Place the robot arm straight and run this code to calibrate it.