#include "stdio.h"
#include "stdbool.h"
#include "stdlib.h"
#include "stdint.h"
#include "math.h"
#include "main.h"
/*
uC speed 68Mhz
  1 instruction = 1/68.000.000 = 0.000000016 0.016uS

  datasheet reports between 500-5000 pps
  motor 17HS19-2004S1
  deg x step = 1.8 means 200pulse for each turn
  
  max velocity is 600rpm
  pps = 600pulse * 200pulgiro / 60sedc = 2000pps
  
  
  
*/

#define DIR_CW GPIO_PIN_SET //Increase the counter
#define DIR_CCW GPIO_PIN_RESET //Decrease the counter

#define TIMER_FREQUENCY 50000 //50Khz
#define PULSE_MAX 2000
#define PULSE_STOP 50
#define PULSE_STEP 10

stepper_t sStepper1;
stepper_t sStepper2;
stepper_t sStepper3;

// Based on the distance 
static int32_t i32CalcPulse;
int32_t desirePulse(int32_t i32StepDiff,int32_t i32Max,int32_t i32Step)
{
  i32CalcPulse = i32StepDiff*i32Step;
  if (i32StepDiff >= 0)
  {
    i32CalcPulse  = (i32CalcPulse > i32Max) ? i32Max : i32CalcPulse;
  }
  else
  {
    i32CalcPulse  = (i32CalcPulse < -i32Max) ? -i32Max : i32CalcPulse;
  }
  return i32CalcPulse;
}

void triggerPulse(stepper_t* psStepper)
{
  if (psStepper->i32ActualPulse >= 0)
  {
    //Set direction to positive
    if (psStepper->bDirActive == DIR_CCW)
    {
      psStepper->bDirActive = DIR_CW;
      HAL_GPIO_WritePin(psStepper->dir.port, psStepper->dir.pin, psStepper->bDirActive);
    }
    //Change actual step counter
    psStepper->i32ActualStep++;
  }
  else
  {
    //set direction to negative
    if (psStepper->bDirActive == DIR_CW)
    {
      psStepper->bDirActive = DIR_CCW;
      HAL_GPIO_WritePin(psStepper->dir.port, psStepper->dir.pin, psStepper->bDirActive);
    }
    //Change actual step counter
    psStepper->i32ActualStep--;    
  }
  //Toggle the step command
  HAL_GPIO_WritePin( psStepper->stp.port, psStepper->stp.pin, GPIO_PIN_SET);
}

static int32_t i32DesirePulse;
static int32_t i32StepDiff;
void evaluateStepper(stepper_t* psStepper)
{
  //always reset the step pin to Low
  if (psStepper->bRunning)
  {
    //Set the step to low (100ns are enough to trigger the step)
    HAL_GPIO_WritePin( psStepper->stp.port, psStepper->stp.pin, GPIO_PIN_RESET);
  }

  if (psStepper->ui32PulseCnt == 0)
  {
    //If emergency stop
    if (psStepper->bEmergencyStop)
    {
      psStepper->bRunning = false;
    }
    
    //If the Position is reached no need we STOP if below the stop threshold
    if (psStepper->i32DesireStep == psStepper->i32ActualStep)
    {
      //Below the PULSE_STOP threshold we can STOP
      if (abs(psStepper->i32ActualPulse) <= psStepper->i32PulseStop)
        psStepper->bRunning = false;
    }
    
    //IF we are keep running
    if (psStepper->bRunning)
    {
      //Check the Difference
      i32StepDiff = psStepper->i32DesireStep - psStepper->i32ActualStep;
      // Check the pulse we should have at this point
      i32DesirePulse =  desirePulse(i32StepDiff, psStepper->i32PulseMax, psStepper->i32PulseStep);

      //Compare actual with desired and ramp the speed
      if (i32DesirePulse > psStepper->i32ActualPulse)
      {
        psStepper->i32ActualPulse += psStepper->i32PulseStep;
        if (psStepper->i32ActualPulse > psStepper->i32PulseMax)
        {
          psStepper->i32ActualPulse = psStepper->i32PulseMax;
        }
      }
      else if (i32DesirePulse < psStepper->i32ActualPulse)
      {
        psStepper->i32ActualPulse -= psStepper->i32PulseStep;
        if (psStepper->i32ActualPulse < -psStepper->i32PulseMax)
        {
          psStepper->i32ActualPulse = -psStepper->i32PulseMax;
        }
      }
      //Trigger Pulse
      triggerPulse(psStepper);
      
      //Update the pulse counter
      psStepper->ui32PulseCnt = TIMER_FREQUENCY/psStepper->i32ActualPulse;
    }
  }
  else
  {
    //Wait for th pulse end
    psStepper->ui32PulseCnt--;
  }
}


/*
  Stepper logic tick timer
  //We want max update rate of 10000pps
  s = 1/100000 = 0.00001 10uS  
*/
volatile uint32_t ui32TimerCounter = 0;
void Timer10msCallback(void)
{

}
void Timer100usCallback(void)
{
  if (ui32TimerCounter == 0)
  {
    Timer10msCallback();
  }
  evaluateStepper(&sStepper1);
  evaluateStepper(&sStepper2);
  evaluateStepper(&sStepper3);
  
  ui32TimerCounter++;
}

void stepperInit(stepper_t *psStepper)
{
  psStepper->i32PulseMax = PULSE_MAX;
  psStepper->i32PulseStop = PULSE_STOP;
  psStepper->i32PulseStep = PULSE_STEP;
  //Set CW
  psStepper->bDirActive = DIR_CW;
  HAL_GPIO_WritePin(psStepper->dir.port, psStepper->dir.pin, DIR_CW);
  //Set enable
  HAL_GPIO_WritePin(psStepper->en.port, psStepper->en.pin, GPIO_PIN_SET);
  psStepper->bRunning = false;
  psStepper->bEmergencyStop = false;
  psStepper->ui32PulseCnt = 0;
  psStepper->i32ActualPulse = 0;
  psStepper->i32ActualStep = 0;
  psStepper->i32DesireStep = 0;
  
}

