/*Initialzie the CANBUS interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0
*/
#include "RMD.h"

//Constructor
RMD_Motor::RMD_Motor(int iSocket, uint16_t ui16NodeId)
{
	this->iSocket = iSocket;
	this->ui16NodeId = ui16NodeId;
};

//Write a command and get the anwer
int RMD_Motor::command(uint8_t *pui8Data)
{
	int nbytes;
	struct can_frame frame;
	
	//Compose request frame, always 8 bytes
	frame.can_id = this->ui16NodeId;
	frame.can_dlc = 8;
	//Fill Frame with data
	memcpy(frame.data,pui8Data,8);
	//Transmit on the Can Bus
	if (write(this->iSocket, &frame, sizeof(struct can_frame)) != sizeof(struct can_frame)) {
		perror("WriteX");
		return 1;
	}

	//If transmission is OK, wait for 8 byte answer
	nbytes = read(this->iSocket, &frame, sizeof(struct can_frame));
	if (nbytes < 0) 
	{
		perror("ReadX");
		return 2;
	}
	
	//Copy content of the can frame to the shared buffer
	memcpy(pui8Data, frame.data,8);

	return 0;						
}

//Set a specific acceleration
//good value seems like 3000
int RMD_Motor::setAcceleration(int16_t i16Acceleration)
{
	this->pBuffer[0] = 0x34;
	this->pBuffer[1] = 0x0;
	this->pBuffer[2] = 0x0;
	this->pBuffer[3] = 0x0;
	this->pBuffer[4] = i16Acceleration & 0xFF;
	this->pBuffer[5] = (i16Acceleration>>8) & 0xFF;
	this->pBuffer[6] = (i16Acceleration>>16) & 0xFF;
	this->pBuffer[7] = (i16Acceleration>>24) & 0xFF;
	return command(this->pBuffer);
	
};

// Read Multi Turn
// value saved is °*100
int RMD_Motor::getPosition()
{
	int64_t i64Tmp = 0;
	memset(this->pBuffer,0,8);
	this->pBuffer[0] = 0x92;
	if (command(this->pBuffer) == 0)
	{
		//Transmit data is a uint64_t but only 7 bytes are transmitted
		//MSB is a copy of the last MSB 
		this->pBuffer[8] =  this->pBuffer[7];
		for (int i = 0; i < 8; i++)
		{
			i64Tmp += this->pBuffer[i+1] << (8*i);
		}
		this->i64Position = i64Tmp;
		return 0;
	}
	return 1;			
};

//Go to multiturn position in °*100 at max speed of
int RMD_Motor::goPosition(int32_t i32Position, uint16_t maxSpeed)
{
	this->pBuffer[0] = 0xA4;
	this->pBuffer[1] = 0x0;
	this->pBuffer[2] = maxSpeed & 0xFF;
	this->pBuffer[3] = (maxSpeed>>8) & 0xFF;
	this->pBuffer[4] = i32Position & 0xFF;
	this->pBuffer[5] = (i32Position>>8) & 0xFF;
	this->pBuffer[6] = (i32Position>>16) & 0xFF;
	this->pBuffer[7] = (i32Position>>24) & 0xFF;
	return command(this->pBuffer);
};

// Read Encoder
int RMD_Motor::getEncoderPosition()
{
	uint16_t ui16Tmp = 0;
	memset(this->pBuffer,0,8);
	this->pBuffer[0] = 0x90;
	if (command(this->pBuffer) == 0)
	{
		//Encoder
		ui16Tmp = this->pBuffer[2] ;
		ui16Tmp += (this->pBuffer[3] <<8);
		this->ui16EncoderPosition = ui16Tmp;
		//Encoder RAW
		ui16Tmp = this->pBuffer[4] ;
		ui16Tmp += (this->pBuffer[5] <<8);
		this->ui16EncoderPositionRaw = ui16Tmp;
		//Encoder Offset
		ui16Tmp = this->pBuffer[6] ;
		ui16Tmp += (this->pBuffer[7] <<8);
		this->ui16EncoderOffset = ui16Tmp;
		return 0;
	}
	return 1;			
};

//Set actual position as 0 position for the internal motor
//Writes an offset - we use this to be able to work with the motor without calibrating it every time
//its important that when the motor is powerd on, the arm is in the init position		
int RMD_Motor::calibrate()
{
	//int16_t i16CalibratePosition;
	//Set actual encoder position to 0
	// this->pBuffer[0] = 0x19;
	// this->pBuffer[1] = 0;
	// this->pBuffer[2] = 0;
	// this->pBuffer[3] = 0;
	// this->pBuffer[4] = 0;
	// this->pBuffer[5] = 0;
	// this->pBuffer[6] = 0;
	// this->pBuffer[7] = 0;
	// return command(this->pBuffer);
	if (getEncoderPosition() != 0)
	{
		//Calibration fail
		return 1;
	}
	printf("RAW data:%i\t%i\t%i\n",this->ui16EncoderPositionRaw,this->ui16EncoderOffset,this->ui16EncoderPosition);
	return 0;
};

int RMD_Motor::calibrate(uint16_t ui16RelativeOffset)
{
	uint16_t uiTmp1,uiTmp2,uiTmp3;
	//Get postion
	if (getEncoderPosition() != 0)
	{
		//Calibration fail
		return 1;
	}
	printf("RAW data:%i\t%i\t%i\n",this->ui16EncoderPositionRaw,this->ui16EncoderOffset,this->ui16EncoderPosition);
	
	//We need to take the actual "position" and add/sub 180° to it, also consider possible motor turns
	//If motor reads 0° we want to set it at 180°, we need to subtract this value then
	//if motor reads 180 we want to set 360 that is 0
	//if motor reads 270 we want the motor to be 180, we need to set the offset to 270-180
	//i16CalibratePosition  = this->i16EncoderPositionRaw - 18000;
	//Tranmsitted data is 16bit value for 1 turn 0-0xFFFF
	//180 is 0x8000 = 32768
	//can we simple subtract 180 ?
	uiTmp1 = this->ui16EncoderPositionRaw - ui16RelativeOffset;
	uiTmp2 = uiTmp1 + ui16RelativeOffset;
	uiTmp3 = this->ui16EncoderPositionRaw - this->ui16EncoderOffset;
	printf("MOD data:%i\t%i\t%i\n",uiTmp1,uiTmp2,uiTmp3);

	// Set actual encoder position to 180
	// First actualize motor position
	this->pBuffer[0] = 0x91;
	this->pBuffer[1] = 0;
	this->pBuffer[2] = 0;
	this->pBuffer[3] = 0;
	this->pBuffer[4] = 0;
	this->pBuffer[5] = 0;
	this->pBuffer[6] = uiTmp1 & 0xFF;
	this->pBuffer[7] = (uiTmp1>>8)&0xFF;
	return command(this->pBuffer);
};


//Turn off the arm
void RMD_Motor::cmdOff()
{
	this->pBuffer[0] = 0x81;
	this->pBuffer[1] = 0;
	this->pBuffer[2] = 0;
	this->pBuffer[3] = 0;
	this->pBuffer[4] = 0;
	this->pBuffer[5] = 0;
	this->pBuffer[6] = 0;
	this->pBuffer[7] = 0;
	command(this->pBuffer);
};

//STOP the command
void RMD_Motor::cmdStop()
{
	this->pBuffer[0] = 0x80;
	this->pBuffer[1] = 0;
	this->pBuffer[2] = 0;
	this->pBuffer[3] = 0;
	this->pBuffer[4] = 0;
	this->pBuffer[5] = 0;
	this->pBuffer[6] = 0;
	this->pBuffer[7] = 0;
	command(this->pBuffer);
};

//Resume after a STOP
void RMD_Motor::cmdRun()
{
	this->pBuffer[0] = 0x88;
	this->pBuffer[1] = 0;
	this->pBuffer[2] = 0;
	this->pBuffer[3] = 0;
	this->pBuffer[4] = 0;
	this->pBuffer[5] = 0;
	this->pBuffer[6] = 0;
	this->pBuffer[7] = 0;
	command(this->pBuffer);
};
	

// Initialize the Canbus 
// return of the idx socket to be used
int initCanbus(int* pSocket)
{
	struct ifreq ifr;
	struct sockaddr_can addr;
	int s;

	if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
		perror("Socket");
		return 1;
	}

	strcpy(ifr.ifr_name, "can0" );
	ioctl(s, SIOCGIFINDEX, &ifr);

	memset(&addr, 0, sizeof(addr));
	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("Bind");
		return 1;
	}
	
	//Set socket timeout intervall
	timeval tv;
	tv.tv_sec = 0;
	tv.tv_usec = 10000;
	setsockopt(s, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

	//Copy socket value
	*pSocket = s;
	return 0;
	
}
