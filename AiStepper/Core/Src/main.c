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
#include "TMC2209.h"
//#include "stm32g0xx_hal_uart.h"

#include "string.h"
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
#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
#define BYTE_TO_BINARY(byte)  \
  ((byte) & 0x80 ? '1' : '0'), \
  ((byte) & 0x40 ? '1' : '0'), \
  ((byte) & 0x20 ? '1' : '0'), \
  ((byte) & 0x10 ? '1' : '0'), \
  ((byte) & 0x08 ? '1' : '0'), \
  ((byte) & 0x04 ? '1' : '0'), \
  ((byte) & 0x02 ? '1' : '0'), \
  ((byte) & 0x01 ? '1' : '0') 
	
/* Asse X
  #pturn = 200pulses turn
	#turns = 5
	#start freq 100
	#maxfreq 200
	#maxacc = 1
*/
#define X_TURN_PULSES 200 //must be an odd number
#define X_TURNS 5
#define X_TOTAL_PULSES (X_TURN_PULSES * X_TURNS)
#define X_HALF_PULSES (X_TOTAL_PULSES/2)
#define X_MIN_PULSE 5
#define X_MAX_PULSE 800
#define X_ACC_PULSE 5
#define X_TIM_CLK 100000

uint16_t aui32XBuffer[X_HALF_PULSES];
uint8_t ui8XState = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
void TIM_DMADelayPulseCplt(DMA_HandleTypeDef *hdma);
void TIM_DMADelayPulseNCplt(DMA_HandleTypeDef *hdma);
void TIM_DMAErrorCCxN(DMA_HandleTypeDef *hdma);

void TIM_CCxNChannelCmd(TIM_TypeDef *TIMx, uint32_t Channel, uint32_t ChannelNState);

HAL_StatusTypeDef HAL_TIM_PWM_Start_DMA2(TIM_HandleTypeDef *htim, uint32_t Channel, const uint32_t *pData,
                                        uint16_t Length);
HAL_StatusTypeDef HAL_TIMEx_PWMN_Start_DMA2(TIM_HandleTypeDef *htim, uint32_t Channel, const uint32_t *pData,
                                           uint16_t Length);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

TMC2209TypeDef tmc2209;
ConfigurationTypeDef sConfig;
void tmc2209_readWriteArray(uint8_t channel, uint8_t *data, size_t writeLength, size_t readLength);
uint8_t tmc2209_CRC8(uint8_t *data, size_t length);


uint32_t ui32Read;
char buff[5] = "ciao";
uint32_t milli;
uint8_t ui8Tmp;
uint8_t ui8Buffer[10];

uint32_t ui32Tmp0;
uint32_t ui32Tmp1;
uint32_t ui32Tmp2;
uint32_t ui32BootTime;
uint8_t aui8StringBuffer[256];
uint8_t ui8StringLen;

volatile uint32_t ui32CounterPeriod = 0;
volatile uint32_t ui32CounterPulse = 0;
uint32_t ui32TimerWait;

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	uint32_t ui32Idx;
	uint16_t pulse = X_MIN_PULSE ;
	uint16_t CounterPeriod;
	uint8_t ui8Tmp1;
	uint8_t ui8Tmp2;
	uint8_t ui8Tmp3;
	uint8_t ui8Tmp4;
	
	//Fill bulses
	for( ui32Idx = 0; ui32Idx < (X_TOTAL_PULSES/2); ui32Idx++)
	{
		CounterPeriod = X_TIM_CLK / pulse;
		aui32XBuffer[ui32Idx] = CounterPeriod;
		pulse += X_ACC_PULSE;
		if (pulse > X_MAX_PULSE)
		{
			pulse = X_MAX_PULSE;
		}	
	}

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
	
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_RESET);
	HAL_Delay(10);
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_SET);
	HAL_Delay(10);
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_SET);
	HAL_Delay(10);
//	//HAL_GPIO_WritePin(XDIR_GPIO_Port,XDIR_Pin, GPIO_PIN_SET);
	tmc_fillCRC8Table(0x07, true, 1);
//	
//	ui8Buffer[0] =  0x5;
//	ui8Buffer[1] =  0x0;
//	ui8Buffer[2] =  0x0;
// 	ui8Buffer[3] =  tmc2209_CRC8(ui8Buffer,3);
//	tmc2209_readWriteArray(0, ui8Buffer,4,8);
//	
//	ui8Buffer[0] =  0x5;
//	ui8Buffer[1] =  0x1;
//	ui8Buffer[2] =  0x0;
// 	ui8Buffer[3] =  tmc2209_CRC8(ui8Buffer,3);
//	tmc2209_readWriteArray(0, ui8Buffer,4,8);

//	ui8Buffer[0] =  0x5;
//	ui8Buffer[1] =  0x2;
//	ui8Buffer[2] =  0x0;
// 	ui8Buffer[3] =  tmc2209_CRC8(ui8Buffer,3);
//	tmc2209_readWriteArray(0, ui8Buffer,4,8);

//	ui8Buffer[0] =  0x5;
//	ui8Buffer[1] =  0x3;
//	ui8Buffer[2] =  0x0;
// 	ui8Buffer[3] =  tmc2209_CRC8(ui8Buffer,3);
//	tmc2209_readWriteArray(0, ui8Buffer,4,8);

	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_SET);

	tmc2209_init(&tmc2209, 0, 0, &sConfig, tmc2209_defaultRegisterResetState);
	tmc2209_periodicJob(&tmc2209,HAL_GetTick());
	tmc2209_reset(&tmc2209);
	
	
	
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	ui32BootTime = HAL_GetTick();
  while (1)
  {
//		//CDC_Transmit_FS((uint8_t*)buff,5);
		milli = HAL_GetTick();
  	tmc2209_periodicJob(&tmc2209,milli);	
		HAL_Delay(1);
		if (tmc2209.config->state == CONFIG_READY)
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
				ui32Tmp0 = tmc2209_readInt(&tmc2209,TMC2209_GCONF);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,0x6c);				
				ui32Tmp0 = TMC2209_FIELD_READ(&tmc2209, TMC2209_CHOPCONF, TMC2209_MRES_MASK, TMC2209_MRES_SHIFT);
				ui32Tmp0 = 256 >> ui32Tmp0;

				ui32Tmp0 = 0;
				//Set the microstef by software

				//TMC2209_FIELD_UPDATE(&tmc2209, TMC2209_CHOPCONF, TMC2209_MRES_MASK, TMC2209_MRES_SHIFT, ui32Tmp0);

				ui32Tmp0 = 256 >> TMC2209_FIELD_READ(&tmc2209, TMC2209_CHOPCONF, TMC2209_MRES_MASK, TMC2209_MRES_SHIFT);
				
				ui32Tmp0 = tmc2209_readInt(&tmc2209,0x6c);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,1);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,2);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,3);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,4);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,5);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,6);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,7);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,8);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,9);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,10);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,11);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,12);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,13);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,14);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,18);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,16);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,17);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,18);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,19);
				ui32Tmp0 = tmc2209_readInt(&tmc2209,20);				
				
				ui8XState = 2;
				HAL_GPIO_WritePin(XEN_GPIO_Port, XEN_Pin, GPIO_PIN_RESET);
				HAL_GPIO_WritePin(XDIR_GPIO_Port, XDIR_Pin, GPIO_PIN_SET);
				HAL_Delay(100);

				if (HAL_TIMEx_PWMN_Start_IT(&htim15,TIM_CHANNEL_1) == HAL_OK)
				{
					//HAL_TIM_PWM_Start_DMA2(&htim15, TIM_CHANNEL_1, (uint32_t)*aui32XBuffer, X_TOTAL_PULSES);
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
						//HAL_TIM_PWM_Start_DMA2(&htim15, TIM_CHANNEL_1, (uint32_t)*aui32XBuffer, X_TOTAL_PULSES);
					}							
				}
			}

		}

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
	


void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* Prevent unused argument(s) compilation warning */
  UNUSED(htim);

	if (htim == &htim7)
	{
    Timer100usCallback();
	}
	if (htim == &htim15)
	{
		ui32CounterPeriod++;
	}
}

void HAL_TIM_PWM_PulseFinishedCallback(TIM_HandleTypeDef *htim)
{
	static uint16_t ui16Value = 0;
	if (htim == &htim15)
	{
		if (ui32CounterPulse < X_HALF_PULSES)
		{
			htim15.Instance->ARR = aui32XBuffer[ui32CounterPulse++];
		}
		else if (ui32CounterPulse < X_TOTAL_PULSES)
		{
			ui16Value = (ui32CounterPulse++) - X_HALF_PULSES ;
			htim15.Instance->ARR = aui32XBuffer[X_HALF_PULSES - ui16Value - 1];
		}
	//	else if (ui32CounterPulse < DMA_BUFFER_SIZE*9)
	//		htim15.Instance->ARR = ui32DmaBuffer[DMA_BUFFER_SIZE-1];
	//	else if (ui32CounterPulse < DMA_BUFFER_SIZE*10)
	//		htim15.Instance->ARR = ui32DmaBuffer[DMA_BUFFER_SIZE-(ui32CounterPulse%DMA_BUFFER_SIZE)];
		else
		{
			HAL_GPIO_TogglePin(XDIR_GPIO_Port, XDIR_Pin);
			ui32CounterPulse = 0xFFFFFFFE;
			ui32CounterPeriod++;	
			HAL_TIMEx_PWMN_Stop_IT(&htim15,TIM_CHANNEL_1);
			//HAL_GPIO_WritePin(XEN_GPIO_Port, XEN_Pin, GPIO_PIN_SET);			
		}	
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
