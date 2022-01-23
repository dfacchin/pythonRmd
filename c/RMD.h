/*Initialzie the CANBUS interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0
*/
#include<stdio.h>
#include "stdint.h"

//cin cout functions
//#include <iostream>
//using namespace std;

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <linux/can.h>
#include <linux/can/raw.h>

class RMD_Motor
{
	public:	
		//Reference to Socket where the motor is connected
		int iSocket;
		//Motor ID identifier
		uint16_t ui16NodeId;
		//Buffer need is 8, Add 1 extra for fast int64 transform
		uint8_t pBuffer[9]; 
		//Last read position
		int64_t i64Position;
		
		//Constructor
		RMD_Motor(int iSocket, uint16_t ui16NodeId);

		//Write a command and get the anwer
		int command(uint8_t *pui8Data);
		
		//Set a specific acceleration
		//good value seems like 3000
		int setAcceleration(int16_t i16Acceleration);		

		// Read Multi Turn
		// value saved is °*100
		int getPosition();
	
		//Go to multiturn position in °*100 at max speed of
		int goPosition(int32_t i32Position, uint16_t maxSpeed);
		
		//Set actual position as 0 position for the internal motor
		//Writes an offset - we use this to be able to work with the motor without calibrating it every time
		//its important that when the motor is powerd on, the arm is in the init position		
		int calibrate();

		//Turn off the arm
		void cmdOff();
		
		//STOP the command
		void cmdStop();
		
		//Resume after a STOP
		void cmdRun();
			
	
};

// Initialize the Canbus 
// return of the idx socket to be used
int initCanbus(int* pSocket);
