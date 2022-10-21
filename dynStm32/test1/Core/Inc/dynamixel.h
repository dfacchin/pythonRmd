/*
 * dynamixel.h
 *
 *  Created on: 17 ott 2022
 *      Author: lele
 */

#ifndef INC_DYNAMIXEL_H_

#include "stdint.h"
#include "stdbool.h"
#include "stdio.h"
#include "string.h"

#define INC_DYNAMIXEL_H_

#define Model_Number (0)
#define Model_Information (2)
#define Firmware_Version (6)
#define ID (7)
#define Baud_Rate (8)
#define Return_Delay_Time (9)
#define Drive_Mode (10)
#define Operating_Mode (11)
#define Secondary_Shadow__ID (12)
#define Protocol_Type (13)
#define Homing_Offset (20)
#define Moving_Threshold (24)
#define Temperature_Limit (31)
#define Max_Voltage_Limit (32)
#define Min_Voltage_Limit (34)
#define PWM_Limit (36)
#define Velocity_Limit (44)
#define Max_Position_Limit (48)
#define Min_Position_Limit (52)
#define Startup_Configuration (60)
#define Shutdown (63)
#define Torque_Enable (64)
#define LED (65)
#define Status_Return_Level (68)
#define Registered_Instruction (69)
#define Hardware_Error_Status (70)
#define Velocity_I_Gain (76)
#define Velocity_P_Gain (78)
#define Position_D_Gain (80)
#define Position_I_Gain (82)
#define Position_P_Gain (84)
#define Feedforward_2nd_Gain (88)
#define Feedforward_1st_Gain (90)
#define Bus_Watchdog (98)
#define Goal_PWM (100)
#define Goal_Velocity (104)
#define Profile_Acceleration (108)
#define Profile_Velocity (112)
#define Goal_Position (116)
#define Realtime_Tick (120)
#define Moving (122)
#define Moving_Status (123)
#define Present_PWM (124)
#define Present_Load (126)
#define Present_Velocity (128)
#define Present_Position (132)
#define Velocity_Trajectory (136)
#define Position_Trajectory (140)
#define Present_Input_Voltage (144)
#define Present_Temperature (146)

typedef struct
{
uint16_t ui16Pos;
uint8_t ui8Size;
} memory_t;

typedef struct
{
bool     bValid;
uint8_t  ui8Id;
uint8_t  ui8Instruction;
uint8_t  ui8Error;
uint16_t ui16Length;
uint16_t ui16Crc;
uint8_t* pui8Buffer;
uint16_t ui16Address;
} dynPacket_t;

typedef struct
{
uint8_t  ui8Id;
uint8_t  ui8Torque;        // 1:enable 0:disable
uint8_t  ui8DrivingMode;   // cw:0 ccw:1
uint8_t  ui8OperatingMode; // multi turn
uint16_t ui16PwmLimit;     // 0-885
uint16_t ui16Velocity;     // 0-885
uint16_t ui16GoalPosition;
uint16_t ui16GoalVelocity;
uint16_t ui16GoalPwm;
uint16_t ui16PresentLoad;
dynPacket_t request;
dynPacket_t response;
} dyn_t;

extern dyn_t dyn;
// RX buffer
extern uint8_t pui8BufferRX[1024];
// TX buffer
extern uint8_t pui8BufferTX[1024];
//MemoryMapping
extern uint8_t dynBuffer[1024];

bool dynamixelInit(dyn_t *psDyn, uint8_t ui8Id);
bool getValue(uint16_t ui16ID,uint32_t *pui32Value);
bool setValue(uint16_t ui16ID,uint32_t ui32Value);
uint16_t encode_packet(dyn_t * psDyn, uint8_t * pui8Buffer);
bool decode_packet(dyn_t * psDyn, uint8_t * pui8Buffer, uint16_t ui16Size);




#endif /* INC_DYNAMIXEL_H_ */
