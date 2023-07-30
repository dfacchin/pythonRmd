#ifndef __AISTEPPER_H
#define __AISTEPPER_H

#include "TMC2209.h"
#include "tim.h"
#include "string.h"

#define AIGD_MOTOR_INIT_TIMER 300
#define AIGD_MOTOR_SPEED_CALIBRATION 50
#define AIGD_MOTOR_THRESHOLD_CALIBRATION 50
#define AIGD_MOTOR_PULSE_MIN_S 50
#define AIGD_MOTOR_PULSE_MAX_S 800
#define AIGD_MOTOR_PULSE_ACCELERATION (1)
#define AIGD_MOTOR_DIFF_PULSE_S (AIGD_MOTOR_PULSE_MAX_S-AIGD_MOTOR_PULSE_MIN_S)



#define AIGD_MOTOR_STATE_NOINIT 0
#define AIGD_MOTOR_STATE_IDLE   1
#define AIGD_MOTOR_STATE_MOVING 2
#define AIGD_MOTOR_STATE_ERROR  3


#define X_TURN_PULSES 200 //must be an odd number
#define X_TURNS 5
#define X_TOTAL_PULSES (X_TURN_PULSES * X_TURNS)
#define X_HALF_PULSES (X_TOTAL_PULSES/2)
#define X_MIN_PULSE 5
#define X_MAX_PULSE 800
#define X_ACC_PULSE 5
#define X_TIM_CLK 100000

typedef struct
{
	//stepper 
	/*	STATE
		0 no init
	  1 idle
	  2 moving
	  3 error
	*/
	int8_t i8Direction;
	uint8_t ui8State;

	uint32_t ui32StepAcc;
	uint32_t ui32StepDec;
	uint32_t ui32StepPulse;

	
	uint32_t ui32Clock;
	uint32_t ui32MaxSteps;
	int32_t i32TargetPosition;
	int32_t i32TargetPositionPrev;
	int32_t i32ActualPosition;
	uint32_t ui32MaxPulseTime;
	uint32_t ui32MinPulseTime;
	uint32_t ui32MaxAcceleration;
	uint32_t ui32Acceleration;
	uint32_t ui32Idx;
	//STM32 pin and timer
	GPIO_TypeDef *EnPort;
	uint16_t EnPin;
	GPIO_TypeDef *DirPort;
	uint16_t DirPin;
	TIM_HandleTypeDef *psHTim;
  //tmc driver
	TMC2209TypeDef tmc2209;
	ConfigurationTypeDef sConfig;
	
	void (*pfStart)(void);
	void (*pfStop)(void);
} motorCtrl_t;


void tmc2209_readWriteArray(uint8_t channel, uint8_t *data, size_t writeLength, size_t readLength);
uint8_t tmc2209_CRC8(uint8_t *data, size_t length);

//Stepper commands
// INIT
bool aiStepper_init(motorCtrl_t *psMotor);
// RUN
void aiStepper_run(motorCtrl_t *psMotor);
// SET ACTUAL STEPPER COUNTER
void aiStepper_setStep(motorCtrl_t *psMotor, int32_t i32Step);
// FIND MECHANICAL LIMIT
bool aiStepper_calibrate(motorCtrl_t *psMotor, int32_t i32ExpectedStep, uint32_t ui32Speed);
// MOTOR INTERRUPT
void motor_interrupt(motorCtrl_t *psMotor);
// MOVE TO 
void aiStepper_moveTo(motorCtrl_t *psMotor, int32_t ui32DesPos);


#endif