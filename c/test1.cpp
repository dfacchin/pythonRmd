/*Initialzie the CANBUS interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0
*/
#include <stdio.h>
#include "stdint.h"

#include "RMD.h"

//cin cout functions
//#include <iostream>
//using namespace std;

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
	
	
	#if (1)	
		if (motor1.calibrate(0x8000) != 0)
			printf("Something Wrong in the calibration process\n");
	#endif
	#if (1)	
		while(true)
		{
			if (motor1.calibrate() != 0)
				printf("Something Wrong in the calibration process\n");
		}
	#endif
		
	
	
	//Get Motor Position
	#if (0)
		motor1.getPosition();
		printf("Position: %li\n",motor1.i64Position);
		printf("Position: %.2f\n",(float)motor1.i64Position/100);
	#endif

	//Set Max Acceleration
	#if (0)
		printf("Set Acceleration\n");
		motor1.setAcceleration(1000);
	#endif

	//Go to specific Position
	#if(0)
		//std::cout << "Enter Desired position\n";
		int32_t i32DesiredPos = -500000;
		//std::cin >> i32DesiredPos;
		motor1.goPosition(i32DesiredPos,2000);
		do
		{
			printf("Ret:%i\t",motor1.getPosition());
			printf("Position: %li\n",motor1.i64Position);
			printf("Position: %li\n",abs(i32DesiredPos - motor1.i64Position));
		//} while (abs(i32DesiredPos - motor1.i64Position) > 100);
		} while (true);
	#endif
	return 0;
}