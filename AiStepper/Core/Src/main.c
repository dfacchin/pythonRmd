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

TMC2209TypeDef tmc2209;
ConfigurationTypeDef sConfig;
void tmc2209_readWriteArray(uint8_t channel, uint8_t *data, size_t writeLength, size_t readLength);
uint8_t tmc2209_CRC8(uint8_t *data, size_t length);


uint32_t ui32Read;
char buff[5] = "ciao";
uint32_t milli;
uint8_t ui8Tmp;
uint8_t ui8Buffer[10];
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

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
  /* USER CODE BEGIN 2 */
	
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_RESET);
	HAL_Delay(10);
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_SET);
	HAL_Delay(10);
	HAL_GPIO_WritePin(XEN_GPIO_Port,XEN_Pin, GPIO_PIN_RESET);
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
  while (1)
  {
		//CDC_Transmit_FS((uint8_t*)buff,5);
		milli = HAL_GetTick();
  	tmc2209_periodicJob(&tmc2209,milli);	
		HAL_Delay(1);
		if (tmc2209.config->state == CONFIG_READY)
		{
			ui8Tmp = tmc2209_readInt(&tmc2209,TMC2209_GCONF);
		}
		HAL_GPIO_TogglePin(XSTP_GPIO_Port,XSTP_Pin);
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

	if (htim == &htim7)
	{
    Timer100usCallback();
	}
}

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
		while( ui8gIdxRx < (writeLength+readLength) ) ui8gIdx++;
		memcpy(data,&aui8gDataIn[writeLength],readLength);
		LL_USART_DisableIT_ERROR(USART4);
		LL_USART_DisableIT_RXNE(USART4);
	}
}
	


//void tmc2209_readWriteArray2(uint8_t channel, uint8_t *data, size_t writeLength, size_t readLength)
//{
//	HAL_StatusTypeDef ret;
//	ret = HAL_OK;
//	//ret = HAL_HalfDuplex_EnableTransmitter(&huart4);
//	if (ret == HAL_OK)
//	{
//		ret = HAL_UART_Transmit(&huart4,data,writeLength,5);
//		if (ret == HAL_OK)
//		{
//			//ret = HAL_HalfDuplex_EnableReceiver(&huart4);
//			//HAL_Delay(1);
//			__HAL_UART_FLUSH_DRREGISTER(&huart4);
//			if (readLength > 0)
//			{
//				//memset(data,0xff,writeLength);
//				if (ret == HAL_OK)
//				{
//					//ret = HAL_UARTEx_ReceiveToIdle(&huart4,data,readLength,&readLength,100);
//					ret = HAL_UART_Receive(&huart4,data,readLength,100);
//					if (ret == HAL_OK)
//					{
//						return;
//					}
//				}
//			}
//			else
//			{
//				return;
//			}
//		}
//	}
//	return;
////	uart->rxtx.clearBuffers();
////	uart->rxtx.txN(data, writeLength);
////	Hal_
////	/* Workaround: Give the UART time to send. Otherwise another write/readRegister can do clearBuffers()
////	 * before we're done. This currently is an issue with the IDE when using the Register browser and the
////	 * periodic refresh of values gets requested right after the write request.
////	 */
////	wait(2);

////	// Abort early if no data needs to be read back
////	if (readLength <= 0)
////		return 0;

////	// Wait for reply with timeout limit
////	uint32_t timestamp = systick_getTick();
////	while(uart->rxtx.bytesAvailable() < readLength)
////	{
////		if(timeSince(timestamp) > UART_TIMEOUT_VALUE)
////		{
////			// Abort on timeout
////			return -1;
////		}
////	}

////	uart->rxtx.rxN(data, readLength);

////	return 0;
//}


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
