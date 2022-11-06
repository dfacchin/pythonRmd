/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
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
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "dynamixel.h"
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

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */


/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint16_t ui16gPwm = 1500;
uint16_t ui16gPwmACtual = 1500;
uint16_t ui16AngleMin = 500;
uint16_t ui16AngleMax = 2500;
uint16_t ui16AngleX10 = 2700;
uint16_t ui16AngleCenter = 1350;

uint16_t ui16LenRxLen;
uint16_t ui16LenTxLen;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	  uint32_t ui32Val;
	  uint32_t ui32Val2;
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
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_1);
  htim2.Instance->CCR1 = 1500;
  dynamixelInit(&dyn, 3);


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	  if(HAL_UARTEx_ReceiveToIdle(&huart1, pui8BufferRX, 256, &ui16LenRxLen, 100) == HAL_OK)
	  {
		  //decode packet
		  if (decode_packet(&dyn, pui8BufferRX, ui16LenRxLen) == true)
		  {
			  if (dyn.request.bValid)
			  {
				  dyn.response.ui8Instruction = dyn.request.ui8Instruction;
				  dyn.response.ui8Id = dyn.ui8Id;
				  dyn.response.pui8Buffer = &pui8BufferTX[9];
				  dyn.response.ui8Error = 0;
				  switch (dyn.request.ui8Instruction)
				  {
					  //Ping
					  case 0x1:
					  dyn.response.pui8Buffer[0] = 0x06; //Fake XM430 W210
					  dyn.response.pui8Buffer[1] = 0x04;
					  dyn.response.pui8Buffer[2] = 0x26;
					  dyn.response.ui16Length = 3;
					  break;

					  //Read Address
					  case 0x2:
					  dyn.response.ui16Address = dyn.request.ui16Address;
					  dyn.response.ui16Length = dyn.request.ui16Length; //Request data and Address
					  memcpy(&dyn.response.pui8Buffer[0], &dynBuffer[dyn.request.ui16Address], dyn.request.ui16Length);

					  break;
					  //Write Address
					  case 0x3:
					  dyn.response.ui16Length = 0;
					  memcpy(&dynBuffer[dyn.request.ui16Address],dyn.request.pui8Buffer, dyn.request.ui16Length);

					  break;
					  default:
					  break;
				  }
				  ui16LenTxLen = encode_packet(&dyn, pui8BufferTX);
				  HAL_Delay(2);
				  if (HAL_UART_Transmit(&huart1, pui8BufferTX, ui16LenTxLen, 150) != HAL_OK)
				  {
					  HAL_Delay(1);
				  }
				  //Clear Uart rx back noise from tx
				  HAL_UART_Abort(&huart1);


			  }
		  }
	  }

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	if (HAL_GetTick() >  1000)
	{
	  //OFF the PWM motor
	  ui16gPwm = 0;
	  if (getValue(Torque_Enable,&ui32Val) == true)
	  {
		  if (ui32Val == 1)
		  {
			  if (getValue(Goal_Position,&ui32Val) == true)
			  {
				  //-135 gradi
				  if (ui32Val<512)
					  ui32Val = 512;
				  //+135
				  if (ui32Val>3584)
					  ui32Val = 3584;
				  //0 is -135
				  ui32Val = ui32Val-512;
				  //convert in ms
				  ui32Val = (ui32Val*2000)/3072;
				  //Convert degree in time pwm

 				  /*
 				   	uint16_t ui16gPwm = 1500;
					uint16_t ui16AngleMin = 500;
					uint16_t ui16AngleMax = 2500;
					uint16_t ui16AngleX10 = 2700;
					uint16_t ui16AngleCenter = 1350;
				   * */
				  if (getValue(Drive_Mode,&ui32Val2) == true)
				  {
					  if ((ui32Val2&0x1)==1)
					  {
						  ui16gPwm = 2500 - ui32Val;

					  }
					  else
					  {
						  ui16gPwm = 500 + ui32Val;

					  }
				  }



			  }

		  }
	  }

	  htim2.Instance->CCR1 = ui16gPwm;
	  //gPwm += ui8Dir;
	  //ui8Dir *= ((gPwm > 2500)||(gPwm < 500)) ? -1 : 1;
	}
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
  if (HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_MSI;
  RCC_OscInitStruct.MSIState = RCC_MSI_ON;
  RCC_OscInitStruct.MSICalibrationValue = 0;
  RCC_OscInitStruct.MSIClockRange = RCC_MSIRANGE_6;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_MSI;
  RCC_OscInitStruct.PLL.PLLM = 1;
  RCC_OscInitStruct.PLL.PLLN = 40;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV7;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

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
