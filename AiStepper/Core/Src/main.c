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
#include "app_fatfs.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "usb_device.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "TMC2209.h"
#include "app_fatfs.h"
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
TMC2209 tmc1;
TMC2209 tmc2;
TMC2209 tmc3;
TMC2209* tmcArray[3];

HardwareSerial hwSerial;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	hwSerial.setSerial(&huart4);
	tmc1.setup(hwSerial,115200,TMC2209::SERIAL_ADDRESS_0);
	tmc2.setup(hwSerial,115200,TMC2209::SERIAL_ADDRESS_1);
	tmc3.setup(hwSerial,115200,TMC2209::SERIAL_ADDRESS_2);
	tmcArray[0] = &tmc1;
	tmcArray[1] = &tmc1;
	tmcArray[2] = &tmc1;
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
  MX_USB_Device_Init();
  MX_USART4_UART_Init();
  if (MX_FATFS_Init() != APP_OK) {
    Error_Handler();
  }
  MX_SPI1_Init();
  MX_TIM7_Init();
  /* USER CODE BEGIN 2 */
	
	HAL_Delay(20);
	for (int idx = 0; idx < 3; idx++)
	{
		tmcArray[idx]->setRunCurrent(100);
		tmcArray[idx]->enableCoolStep();
		tmcArray[idx]->enable();
	}

//Set hardware pin
  sStepper1.dir.pin = XDIR_Pin;
  sStepper1.dir.port = XDIR_GPIO_Port;
  sStepper1.stp.pin = XSTP_Pin;
  sStepper1.stp.port = XSTP_GPIO_Port;
  sStepper1.en.pin = XEN_Pin;
  sStepper1.en.port = XEN_GPIO_Port;
  sStepper1.stop.pin = X_STOP_Pin;
  sStepper1.stop.port = X_STOP_GPIO_Port;
  //Init structure
  stepperInit(&sStepper1);
  
//Set hardware pin
  sStepper2.dir.pin = YDIR_Pin;
  sStepper2.dir.port = YDIR_GPIO_Port;
  sStepper2.stp.pin = YSTP_Pin;
  sStepper2.stp.port = YSTP_GPIO_Port;
  sStepper2.en.pin = YEN_Pin;
  sStepper2.en.port = YEN_GPIO_Port;
  sStepper2.stop.pin = Y_STOP_Pin;
  sStepper2.stop.port = Y_STOP_GPIO_Port;
  //Init structure
  stepperInit(&sStepper2);

//Set hardware pin
  sStepper3.dir.pin = ZDIR_Pin;
  sStepper3.dir.port = ZDIR_GPIO_Port;
  sStepper3.stp.pin = ZSTP_Pin;
  sStepper3.stp.port = ZSTP_GPIO_Port;
  sStepper3.en.pin = ZEN_Pin;
  sStepper3.en.port = ZEN_GPIO_Port;
  sStepper3.stop.pin = Z_STOP_Pin;
  sStepper3.stop.port = Z_STOP_GPIO_Port;
  //Init structure
  stepperInit(&sStepper3);
	
	HAL_TIM_Base_Start_IT(&htim7);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
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
