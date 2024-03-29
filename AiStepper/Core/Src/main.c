/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "dma.h"
#include "app_fatfs.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "usb_device.h"
#include "gpio.h"


/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "app_fatfs.h"
#include "usbd_cdc_if.h"
#include "aiStepper.h"
//#include "stm32g0xx_hal_uart.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

void criticalError(void)
{
	//Do something to show error state
	while(true)
	{
		HAL_GPIO_TogglePin(BED_PWM_GPIO_Port, BED_PWM_Pin);
		HAL_Delay(200);
	}	
}

void fMotorXStart(void)
{
	HAL_TIMEx_PWMN_Start_IT(&htim15,TIM_CHANNEL_1);
}

void fMotorXStop(void)
{
	HAL_TIMEx_PWMN_Stop_IT(&htim15,TIM_CHANNEL_1);
}
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
motorCtrl_t sMotorX;

uint8_t ui8Test1;
int32_t i32Test1;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
  static uint32_t millis;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART1_UART_Init();
  MX_USB_Device_Init();
  MX_USART4_UART_Init();
  if (MX_FATFS_Init() != APP_OK) {
    Error_Handler();
  }
  MX_SPI1_Init();
  MX_TIM7_Init();
  MX_TIM15_Init();
  /* USER CODE BEGIN 2 */
	//tmc general function
	tmc_fillCRC8Table(0x07, true, 1);
	
	//Prepare motor 1

	sMotorX.DirPort = XDIR_GPIO_Port;
	sMotorX.DirPin = XDIR_Pin;
	sMotorX.EnPort = XEN_GPIO_Port;
	sMotorX.EnPin = XEN_Pin;
	sMotorX.psHTim = &htim15;
	sMotorX.ui32Clock = X_TIM_CLK;
	//motor1 tmc	
	tmc2209_init(&sMotorX.tmc2209, 0, 0, &sMotorX.sConfig, tmc2209_defaultRegisterResetState);
	tmc2209_periodicJob(&sMotorX.tmc2209,HAL_GetTick());
	tmc2209_reset(&sMotorX.tmc2209);
	//specific funcitons
	sMotorX.pfStart = &fMotorXStart;
	sMotorX.pfStop  = &fMotorXStop;
	
		
	//Blink varius leds
	for (millis = 0; millis < 5; millis++)
	{
		HAL_GPIO_TogglePin(FAN0_PWM_GPIO_Port, FAN0_PWM_Pin);
		HAL_Delay(200);
	}

	for (millis = 0; millis < 5; millis++)
	{
		HAL_GPIO_TogglePin(FAN1_PWM_GPIO_Port, FAN1_PWM_Pin);
		HAL_Delay(200);
	}

	for (millis = 0; millis < 5; millis++)
	{
		HAL_GPIO_TogglePin(BED_PWM_GPIO_Port, BED_PWM_Pin);
		HAL_Delay(200);
	}

	for (millis = 0; millis < 5; millis++)
	{
		HAL_GPIO_TogglePin(FAN_PWM_GPIO_Port, FAN_PWM_Pin);
		HAL_Delay(200);
	}
	
	//Init motor 1
	if (aiStepper_init(&sMotorX) == false)
	{
		criticalError();
	}
	
	ui8Test1 = 0;
	
	
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  while (1)
  {
		aiStepper_run(&sMotorX);
		if (ui8Test1 == 1)
		{
		  aiStepper_moveTo(&sMotorX, i32Test1);
			ui8Test1 = 0;
		}
		/*

		if (sMotorX.tmc2209.config->state == CONFIG_READY)
		{
			if (ui8XState == 0)
			{
				if ( ( HAL_GetTick() - ui32BootTime) > 4000)
				{
					ui8XState = 1;
				}
			}


			if (ui8XState == 1)
			{

				if (HAL_TIMEx_PWMN_Start_IT(&htim15,TIM_CHANNEL_1) == HAL_OK)
				{
					//HAL_TIM_PWM_Start_DMA2(&htim15, TIM_CHANNEL_1, (uint32_t)*aui16Buffer, X_TOTAL_PULSES);
				}				
			}
			else if (ui8XState == 2)
			{
				//read current 
				ui32Tmp0 = tmc2209_readInt(&tmc2209, TMC2209_SG_RESULT);
				ui32Tmp1 = tmc2209_readInt(&tmc2209, TMC2209_IOIN);
				ui8Tmp = ui32Tmp1;
				ui32Tmp1 = tmc2209_readInt(&tmc2209, TMC2209_DRVSTATUS);
				ui8Tmp1 = ui32Tmp1&0xFF;
				ui8Tmp2 = (ui32Tmp1>>8)&0xFF;
				ui8Tmp3 = (ui32Tmp1>>16)&0xFF;
				ui8Tmp4 = (ui32Tmp1>>24)&0xFF;
				ui32Tmp2 = tmc2209_readInt(&tmc2209, TMC2209_IFCNT);
				ui8StringLen = sprintf((char*)aui8StringBuffer,"%05.0d %05.0d [ "BYTE_TO_BINARY_PATTERN" ]-"BYTE_TO_BINARY_PATTERN"-"BYTE_TO_BINARY_PATTERN"-"BYTE_TO_BINARY_PATTERN"-"BYTE_TO_BINARY_PATTERN"\n",
						ui32Tmp0,ui32Tmp2,
						BYTE_TO_BINARY(ui8Tmp),
						BYTE_TO_BINARY(ui8Tmp4),
						BYTE_TO_BINARY(ui8Tmp3),
						BYTE_TO_BINARY(ui8Tmp2),
						BYTE_TO_BINARY(ui8Tmp1));
				//ui8StringLen = sprintf((char*)aui8StringBuffer,"%d-%d\n",ui32Tmp0,ui32Tmp1);

				CDC_Transmit_FS(aui8StringBuffer,ui8StringLen);
				HAL_Delay(20);

			}
			else if(ui8XState == 3)				
			{
				HAL_GPIO_WritePin(XEN_GPIO_Port, XEN_Pin, GPIO_PIN_SET);				
			}
			
			if (ui32CounterPulse == 0xFFFFFFFE)
			{
				ui32CounterPulse = 0xFFFFFFFF;
				ui32TimerWait = HAL_GetTick();
				//HAL_GPIO_WritePin(XEN_GPIO_Port, XEN_Pin, GPIO_PIN_SET);
			}
			else if (ui32CounterPulse == 0xFFFFFFFF)
			{
				if ( (HAL_GetTick() - ui32TimerWait) > 2000)
				{
					ui32CounterPulse = 0;
					HAL_GPIO_WritePin(XEN_GPIO_Port, XEN_Pin, GPIO_PIN_RESET);
				}
				if ( (HAL_GetTick() - ui32TimerWait) > 2000)
				{
					ui32CounterPulse = 0;
					if (HAL_TIMEx_PWMN_Start_IT(&htim15,TIM_CHANNEL_1) == HAL_OK)
					{
						//HAL_TIM_PWM_Start_DMA2(&htim15, TIM_CHANNEL_1, (uint32_t)*aui16Buffer, X_TOTAL_PULSES);
					}							
				}
			}

		}
*/
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_HSI48;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSI48State = RCC_HSI48_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = RCC_PLLM_DIV1;
  RCC_OscInitStruct.PLL.PLLN = 16;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */




void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* Prevent unused argument(s) compilation warning */
  UNUSED(htim);

}


void HAL_TIM_PWM_PulseFinishedCallback(TIM_HandleTypeDef *htim)
{
	static uint16_t ui16Value = 0;
	if (htim == sMotorX.psHTim)
	{
		motor_interrupt(&sMotorX);
	}
}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
