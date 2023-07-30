#include "aiStepper.h"
#include "utilis.h"

void aiStepper_setDirection(motorCtrl_t *psMotor)
{
	HAL_GPIO_WritePin(psMotor->DirPort, psMotor->DirPin, (psMotor->i8Direction == 1)? GPIO_PIN_SET:GPIO_PIN_RESET);
}

void aiStepper_generateRamp(motorCtrl_t *psMotor)
{
	int32_t i32Diff = psMotor->i32TargetPosition - psMotor->i32ActualPosition;
	uint32_t pulseTime = 0;
	uint32_t ui32Idx;
	if (i32Diff < 0)
	{
		//Invert the counter
		i32Diff = -i32Diff;
		psMotor->i8Direction = -1;
	}
	else
	{
		psMotor->i8Direction = 1;
	}
	//Set pulse time
	psMotor->ui32StepPulse = psMotor->ui32MinPulseTime;
	//Set the number of pulses to for acceleration and the one for deceleration
	ui32Idx = ((psMotor->ui32MaxPulseTime - psMotor->ui32MinPulseTime)/psMotor->ui32Acceleration);
	if (i32Diff >= (ui32Idx*2))
	{
		psMotor->ui32StepAcc = i32Diff-ui32Idx;
		psMotor->ui32StepDec = ui32Idx;
	}
	else
	{
		psMotor->ui32StepAcc = psMotor->ui32StepDec = i32Diff/2;
	}

	psMotor->ui32Idx = 0;
}

void aiStepper_startMovement(motorCtrl_t *psMotor)
{
	psMotor->pfStart();
	psMotor->ui8State = 2;
}

void aiStepper_moveTo(motorCtrl_t *psMotor, int32_t ui32DesPos)
{
	if (psMotor->i32ActualPosition == ui32DesPos)
	{
		//We are already at this position
		return;
	}
	
	psMotor->i32TargetPosition = ui32DesPos;
	aiStepper_generateRamp(psMotor);
	aiStepper_setDirection(psMotor);
	aiStepper_startMovement(psMotor);
}

bool aiStepper_init(motorCtrl_t *psMotor)
{
	uint32_t ui32Timer = HAL_GetTick();
	while (psMotor->tmc2209.config->state != CONFIG_READY)
  {
		tmc2209_periodicJob(&psMotor->tmc2209, HAL_GetTick());	
		if ( (HAL_GetTick() - ui32Timer) > AIGD_MOTOR_INIT_TIMER)
		{
			return false;
		}
	}
	aiStepper_setStep(psMotor, 0);
	psMotor->ui8State = AIGD_MOTOR_STATE_IDLE;
	psMotor->ui32MaxPulseTime = AIGD_MOTOR_PULSE_MAX_S;
	psMotor->ui32MinPulseTime = AIGD_MOTOR_PULSE_MIN_S;
	psMotor->ui32Acceleration = AIGD_MOTOR_PULSE_ACCELERATION;
		
	return true;
}

// return 
// 0 Motor mechanical limit reached
// 1 Motor reached stepper count
// 2 Motor run in timeout

uint8_t aiStepper_findMechanicalLimit(motorCtrl_t *psMotor, int32_t i32Step, uint32_t ui32Timeout)
{
	uint32_t ui32Timer = HAL_GetTick();
	//start motor movement at slow speed
	while ( (HAL_GetTick() - ui32Timer) < ui32Timeout)
	{
		tmc2209_periodicJob(&psMotor->tmc2209, HAL_GetTick());	
		//check if mechanical limit was found
		
		//Check if the position is reached
		if (psMotor->ui8State == AIGD_MOTOR_STATE_IDLE)
		{
			if ( checkPos(psMotor->i32ActualPosition, i32Step, AIGD_MOTOR_THRESHOLD_CALIBRATION))
			{
				return 1;
			}
		}
	}
	return 2;
}

bool aiStepper_calibrate(motorCtrl_t *psMotor, int32_t i32ExpectedStep, uint32_t ui32Speed)
{
	/* First we go in back direction with low speed and limti detection
	   Second we set counter to -100 (half turn)
	   Third we move of the Expeceted steps +100 at regular speed
		 Firth we move back at low speed to see if the counter are near the desired
	*/
	if (aiStepper_findMechanicalLimit(psMotor, -(psMotor->ui32MaxSteps * 2), AIGD_MOTOR_SPEED_CALIBRATION) != 0)
	{
		//calibration fail
		return false;
	}
	//Set 0 position
	aiStepper_setStep(psMotor,-100);
	//Open
	if (aiStepper_findMechanicalLimit(psMotor, psMotor->ui32MaxSteps, AIGD_MOTOR_SPEED_CALIBRATION) != 1)
	{
		//calibration fail
		return false;
	}
	//Now close again
	if (aiStepper_findMechanicalLimit(psMotor, -(psMotor->ui32MaxSteps * 2), AIGD_MOTOR_SPEED_CALIBRATION) != 0)
	{
		//calibration fail
		return false;
	}
	return true;
}


void aiStepper_run(motorCtrl_t *psMotor)
{
	tmc2209_periodicJob(&psMotor->tmc2209, HAL_GetTick());	

}

void aiStepper_setStep(motorCtrl_t *psMotor, int32_t i32Step)
{
	psMotor->i32ActualPosition = i32Step;
}





//TMC write and read serial
/* Low level TMC data transmission*/
uint8_t aui8gDataOut[16];
uint8_t aui8gDataIn[16];
volatile uint8 ui8gIdxTx;
volatile uint8 ui8gIdx;
volatile uint8 ui8gIdxRx = 0;
volatile uint8_t ui8GlobalFlag = 0;
volatile uint16_t ui8GlobalRx = 0;

void USART_CharReception_Callback(void)
{
	aui8gDataIn[ui8gIdxRx++] = LL_USART_ReceiveData8(USART4);
	ui8gIdxRx%=16;
}

void Error_Callback(void)
{
	if (LL_USART_IsActiveFlag_ORE(USART4))
	{
	  LL_USART_ClearFlag_ORE(USART4);
	}
}
void tmc2209_readWriteArray(uint8_t channel, uint8_t *data, size_t writeLength, size_t readLength)
{
	uint32_t timeout;
	timeout = HAL_GetTick();
	HAL_Delay(2);
	
	ui8gIdx = 0;
	ui8gIdxRx = 0;
  /* Clear Overrun flag, in case characters have already been sent to USART */
	if (readLength>0)
	{
		LL_USART_ReceiveData8(USART4);
		LL_USART_EnableIT_ERROR(USART4);
		LL_USART_EnableIT_RXNE(USART4);
	}
	
	while(ui8gIdx < writeLength)
	{
		LL_USART_TransmitData8(USART4, data[ui8gIdx++]);
		while (!LL_USART_IsActiveFlag_TXE(USART4));
	}
	if(readLength>0)
	{
		//while (!LL_USART_IsActiveFlag_TC(USART4)) ui8gIdx++;
		while( ui8gIdxRx < (writeLength+readLength) ) 
		{
			if ((HAL_GetTick() -timeout) > 50 )
			{
				memset(data,0,readLength);
				LL_USART_DisableIT_ERROR(USART4);
				LL_USART_DisableIT_RXNE(USART4);
				LL_USART_ClearFlag_ORE(USART4);			
			}		
		}
		ui8gIdx++;
		memcpy(data,&aui8gDataIn[writeLength],readLength);
		LL_USART_DisableIT_ERROR(USART4);
		LL_USART_DisableIT_RXNE(USART4);
	  LL_USART_ClearFlag_ORE(USART4);
	}
}
//	
//void motor_interrupt2(motorCtrl_t *psMotor)
//{
//	//Update motor position
//	psMotor->i32ActualPosition += psMotor->i8Direction; 
//	
//	if (psMotor->ui8StepMode == 0)
//	{
//		if (psMotor->ui32Idx < (AIGD_MOTOR_DIFF_PULSE_S*2) )
//		{
//			psMotor->psHTim->Instance->ARR = psMotor->aui16Buffer[psMotor->ui32Idx++];
//		}
//		else
//		{
//			psMotor->pfStop();
//			psMotor->ui8State = 1;
//		}		  
//	}
//	else if (psMotor->ui8StepMode == 10)
//	{
//		if (psMotor->ui32Idx < (AIGD_MOTOR_DIFF_PULSE_S) )
//		{
//			psMotor->psHTim->Instance->ARR = psMotor->aui16Buffer[psMotor->ui32Idx++];
//		}
//		else if (psMotor->ui32Idx < (AIGD_MOTOR_DIFF_PULSE_S*2) )
//		{
//			if (psMotor->ui32ExtraSteps > 0)
//			{
//				psMotor->psHTim->Instance->ARR = psMotor->ui32Clock/psMotor->ui32MaxPulseTime;
//				psMotor->ui32ExtraSteps--;
//			}
//			else
//			{
//				psMotor->psHTim->Instance->ARR = psMotor->aui16Buffer[psMotor->ui32Idx++];
//			}
//		}
//		else
//		{
//			psMotor->pfStop();
//			psMotor->ui8State = 1;			
//		}
//	}
//	else if (psMotor->ui8StepMode == 20)
//	{
//		if (psMotor->ui32Idx < (AIGD_MOTOR_DIFF_PULSE_S - psMotor->ui32SkipSteps/2) )
//		{
//			psMotor->psHTim->Instance->ARR = psMotor->aui16Buffer[psMotor->ui32Idx++];
//		}
//		else 	
//		{
//			psMotor->ui8StepMode = 0;
//			psMotor->ui32Idx += psMotor->ui32SkipSteps;
//			
//		}
//	}
//}

	
void motor_interrupt(motorCtrl_t *psMotor)
{
	//Update motor position
	psMotor->i32ActualPosition += psMotor->i8Direction; 
	if (psMotor->i32ActualPosition == psMotor->i32TargetPosition)
	{
		psMotor->pfStop();
		psMotor->ui8State = 1;	
	}
	if (psMotor->ui32StepAcc > 0)
	{
		psMotor->ui32StepPulse += psMotor->ui32Acceleration;
		if (psMotor->ui32StepPulse > psMotor->ui32MaxPulseTime)
		{
		  psMotor->ui32StepPulse = psMotor->ui32MaxPulseTime;
		}
		psMotor->psHTim->Instance->ARR = psMotor->ui32Clock/psMotor->ui32StepPulse;
		psMotor->ui32StepAcc--;
	} 
	else if (psMotor->ui32StepDec > 0)
	{
		psMotor->ui32StepPulse -= psMotor->ui32Acceleration;
		if (psMotor->ui32StepPulse < psMotor->ui32MinPulseTime)
		{
		  psMotor->ui32StepPulse = psMotor->ui32MinPulseTime;
		}
		psMotor->psHTim->Instance->ARR = psMotor->ui32Clock/psMotor->ui32StepPulse;
		psMotor->ui32StepDec--;
	}
	else
	{
		psMotor->pfStop();
		psMotor->ui8State = 1;
	}
}
