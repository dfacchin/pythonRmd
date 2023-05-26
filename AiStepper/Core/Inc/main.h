/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32g0xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stdbool.h"
typedef struct
{
  GPIO_TypeDef  *port;
  uint32_t pin;
} pint_t;

typedef struct
{
  int32_t i32PulseMax;
  int32_t i32PulseStep;
  int32_t i32PulseStop;
  GPIO_PinState bDirActive;
  bool bRunning;
  bool bEmergencyStop;
  int32_t i32ActualStep;
  int32_t i32DesireStep;
  int32_t i32ActualPulse;
  uint8_t idx;
  uint32_t ui32PulseCnt;
  pint_t dir;
  pint_t stp;
  pint_t en;
  pint_t stop;
} stepper_t;

extern stepper_t sStepper1;
void stepperInit(stepper_t *psStepper);

void Timer100usCallback(void);

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define PC12_Pin GPIO_PIN_12
#define PC12_GPIO_Port GPIOC
#define PS_ON_Pin GPIO_PIN_13
#define PS_ON_GPIO_Port GPIOC
#define PROBE_Pin GPIO_PIN_14
#define PROBE_GPIO_Port GPIOC
#define E0_STOP_Pin GPIO_PIN_15
#define E0_STOP_GPIO_Port GPIOC
#define X_STOP_Pin GPIO_PIN_0
#define X_STOP_GPIO_Port GPIOC
#define Y_STOP_Pin GPIO_PIN_1
#define Y_STOP_GPIO_Port GPIOC
#define Z_STOP_Pin GPIO_PIN_2
#define Z_STOP_GPIO_Port GPIOC
#define SD_DET_Pin GPIO_PIN_3
#define SD_DET_GPIO_Port GPIOC
#define TH0_Pin GPIO_PIN_0
#define TH0_GPIO_Port GPIOA
#define SERVOS_Pin GPIO_PIN_1
#define SERVOS_GPIO_Port GPIOA
#define CD_CS_Pin GPIO_PIN_4
#define CD_CS_GPIO_Port GPIOA
#define THB_Pin GPIO_PIN_4
#define THB_GPIO_Port GPIOC
#define ZDIR_Pin GPIO_PIN_5
#define ZDIR_GPIO_Port GPIOC
#define ZSTP_Pin GPIO_PIN_0
#define ZSTP_GPIO_Port GPIOB
#define ZEN_Pin GPIO_PIN_1
#define ZEN_GPIO_Port GPIOB
#define YDIR_Pin GPIO_PIN_2
#define YDIR_GPIO_Port GPIOB
#define YSTP_Pin GPIO_PIN_10
#define YSTP_GPIO_Port GPIOB
#define YEN_Pin GPIO_PIN_11
#define YEN_GPIO_Port GPIOB
#define XDIR_Pin GPIO_PIN_12
#define XDIR_GPIO_Port GPIOB
#define XSTP_Pin GPIO_PIN_13
#define XSTP_GPIO_Port GPIOB
#define XEN_Pin GPIO_PIN_14
#define XEN_GPIO_Port GPIOB
#define FAN1_PWM_Pin GPIO_PIN_15
#define FAN1_PWM_GPIO_Port GPIOB
#define Neo_Pin GPIO_PIN_8
#define Neo_GPIO_Port GPIOA
#define FAN0_PWM_Pin GPIO_PIN_6
#define FAN0_PWM_GPIO_Port GPIOC
#define FAN_PWM_Pin GPIO_PIN_7
#define FAN_PWM_GPIO_Port GPIOC
#define STATUS_Pin GPIO_PIN_8
#define STATUS_GPIO_Port GPIOD
#define SPI1_CS_Pin GPIO_PIN_9
#define SPI1_CS_GPIO_Port GPIOD
#define BTN_ENC_Pin GPIO_PIN_15
#define BTN_ENC_GPIO_Port GPIOA
#define HE0_PWM_Pin GPIO_PIN_8
#define HE0_PWM_GPIO_Port GPIOC
#define BED_PWM_Pin GPIO_PIN_9
#define BED_PWM_GPIO_Port GPIOC
#define E0EN_Pin GPIO_PIN_1
#define E0EN_GPIO_Port GPIOD
#define LCD_EN_Pin GPIO_PIN_6
#define LCD_EN_GPIO_Port GPIOD
#define E0STP_Pin GPIO_PIN_3
#define E0STP_GPIO_Port GPIOB
#define E0DIR_Pin GPIO_PIN_4
#define E0DIR_GPIO_Port GPIOB
#define BEEPER_Pin GPIO_PIN_5
#define BEEPER_GPIO_Port GPIOB
#define A2_Pin GPIO_PIN_8
#define A2_GPIO_Port GPIOB
#define A1_Pin GPIO_PIN_9
#define A1_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
