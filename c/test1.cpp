/*Initialzie the CANBUS interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0
*/
#include <stdio.h>
#include "stdint.h"

#include "RMD.h"

int main()
{
	int s;

	//Init CAN bus
	if (initCanbus(&s) == 1)
	{
		perror("Can Init error");
		return 1;		
	}
	
	//Init Motor1 idx 141
	RMD_Motor motor1(s,0x141);
	
	//Set motor actual position as 0 position
	#if (0)	
		
		printf("Set motor position as 0 position\n");
		if (motor1.calibrate() == 0)
		{
			printf("\nCalibration Complete, powercycle the motor to take effect\n");
		}
		else
		{
			printf("Something Wrong in the calibration process\n");
		}
	#endif
	
	
	//Get Motor Position
	#if (1)
		motor1.getPosition();
		printf("Position: %li\n",motor1.i64Position);
		printf("Position: %.2f\n",(float)motor1.i64Position/100);
	#endif

	//Set Max Acceleration
	#if (1)
		printf("Set Acceleration\n");
		motor1.setAcceleration(3000);
	#endif

	//Go to specific Position
	#if(1)
		//std::cout << "Enter Desired position\n";
		int32_t i32DesiredPos = 0;
		//std::cin >> i32DesiredPos;
		motor1.goPosition(i32DesiredPos,6000);
		do
		{
			motor1.getPosition();
		} while (abs(i32DesiredPos - motor1.i64Position) < 100);
	#endif
	return 0;
}