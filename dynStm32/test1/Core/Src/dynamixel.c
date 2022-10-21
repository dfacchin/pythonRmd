#include "dynamixel.h"

// Addresses

#define DYN_MAX_ELEMENTS (50)

uint16_t elements[DYN_MAX_ELEMENTS][2] =
	{
		{ Model_Number, 2},
		{ Model_Information, 4},
		{ Firmware_Version, 1},
		{ ID, 1},
		{ Baud_Rate, 1},
		{ Return_Delay_Time, 1},
		{ Drive_Mode, 1},
		{ Operating_Mode, 1},
		{ Secondary_Shadow__ID, 1},
		{ Protocol_Type, 1},
		{ Homing_Offset, 4},
		{ Moving_Threshold, 4},
		{ Temperature_Limit, 1},
		{ Max_Voltage_Limit, 2},
		{ Min_Voltage_Limit, 2},
		{ PWM_Limit, 2},
		{ Velocity_Limit, 4},
		{ Max_Position_Limit, 4},
		{ Min_Position_Limit, 4},
		{ Startup_Configuration, 1},
		{ Shutdown, 1},
		{ Torque_Enable, 1},
		{ LED, 1},
		{ Status_Return_Level, 1},
		{ Registered_Instruction, 1},
		{ Hardware_Error_Status, 1},
		{ Velocity_I_Gain, 2},
		{ Velocity_P_Gain, 2},
		{ Position_D_Gain, 2},
		{ Position_I_Gain, 2},
		{ Position_P_Gain, 2},
		{ Feedforward_2nd_Gain, 2},
		{ Feedforward_1st_Gain, 2},
		{ Bus_Watchdog, 1},
		{ Goal_PWM, 2},
		{ Goal_Velocity, 4},
		{ Profile_Acceleration, 4},
		{ Profile_Velocity, 4},
		{ Goal_Position, 4},
		{ Realtime_Tick, 2},
		{ Moving, 1},
		{ Moving_Status, 1},
		{ Present_PWM, 2},
		{ Present_Load, 2},
		{ Present_Velocity, 4},
		{ Present_Position, 4},
		{ Velocity_Trajectory, 4},
		{ Position_Trajectory, 4},
		{ Present_Input_Voltage, 2},
		{ Present_Temperature, 1}
	};



unsigned short update_crc(unsigned short crc_accum, unsigned char *data_blk_ptr, unsigned short data_blk_size)
{
    unsigned short i, j;
    unsigned short crc_table[256] = {
        0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
        0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
        0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
        0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
        0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
        0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
        0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
        0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
        0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
        0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
        0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
        0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
        0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
        0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
        0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
        0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
        0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
        0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
        0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
        0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
        0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
        0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
        0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
        0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
        0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
        0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
        0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
        0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
        0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
        0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
        0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
        0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
    };

    for(j = 0; j < data_blk_size; j++)
    {
        i = ((unsigned short)(crc_accum >> 8) ^ data_blk_ptr[j]) & 0xFF;
        crc_accum = (crc_accum << 8) ^ crc_table[i];
    }

    return crc_accum;
}


uint16_t mem2ui16(uint8_t *pBuffer, uint16_t ui16Idx)
{
	return (uint16_t) (pBuffer[ui16Idx] + (pBuffer[ui16Idx+1]<<8));
}

// RX buffer
uint8_t pui8BufferRX[1024];
// TX buffer
uint8_t pui8BufferTX[1024];
// Rx data count
uint16_t ui16Rx;
//MemoryMapping
uint8_t dynBuffer[1024];

dyn_t dyn = {.ui8Id = 3};

bool decode_packet(dyn_t * psDyn, uint8_t * pui8Buffer, uint16_t ui16Size)
{
	// CRC variable
	uint16_t ui16Crc;
	psDyn->request.bValid = false;

	if (pui8Buffer[0] != 0xFF)
		return false;
	if (pui8Buffer[1] != 0xFF)
		return false;
	if (pui8Buffer[2] != 0xFD)
		return false;
	if (pui8Buffer[3] != 0x0)
		return false;
	if (pui8Buffer[4] != psDyn->ui8Id)
		return false;
	// Length
	psDyn->request.ui16Length = (pui8Buffer[6] << 8) + pui8Buffer[5];
	// Test length
	if ((psDyn->request.ui16Length+7) != ui16Size )
		return false;
	//At least instruction and CRC
	if ((psDyn->request.ui16Length) < 3 )
		return false;
	// Instruction
	psDyn->request.ui8Instruction = pui8Buffer[7];
	//data keep it in the rx buffer
	psDyn->request.pui8Buffer = &pui8Buffer[8];
	//CRC
	psDyn->request.ui16Crc = (pui8Buffer[ui16Size-1]<<8) + pui8Buffer[ui16Size-2];
	ui16Crc = update_crc(0, pui8Buffer, ui16Size-2);
	//Test CRC
	if (ui16Crc != psDyn->request.ui16Crc)
		return false;
	psDyn->request.bValid = true;


	switch (dyn.request.ui8Instruction)
	{
		//Read and write
		case 0x2:
			//First 2 bytes are the read address
			psDyn->request.ui16Address = (psDyn->request.pui8Buffer[1] << 8) + psDyn->request.pui8Buffer[0];
			//2 bytes are the read size
			psDyn->request.ui16Length = (psDyn->request.pui8Buffer[3] << 8) + psDyn->request.pui8Buffer[2];
			//shift data buffer
			psDyn->request.pui8Buffer = &psDyn->request.pui8Buffer[4];

			break;
		case 0x3:
			//First 2 bytes are the write address
			psDyn->request.ui16Address = (psDyn->request.pui8Buffer[1] << 8) + psDyn->request.pui8Buffer[0];
			//shift data buffer
			psDyn->request.pui8Buffer = &psDyn->request.pui8Buffer[2];
			//remove CRC and instruction
			psDyn->request.ui16Length -= 3;
			//reduce data length
			psDyn->request.ui16Length -= 2;
			break;
		default:
		break;
	}
	return true;
}

uint16_t encode_packet(dyn_t * psDyn, uint8_t * pui8Buffer)
{
	// CRC variable
	uint16_t ui16Crc;
	uint16_t ui16Size;
	psDyn->request.bValid = false;

	pui8Buffer[0] = 0xFF;
	pui8Buffer[1] = 0xFF;
	pui8Buffer[2] = 0xFD;
	pui8Buffer[3] = 0x0;
	pui8Buffer[4] = psDyn->response.ui8Id;
	psDyn->response.ui16Length += 4; //Add response lenght overhead
	pui8Buffer[5] = (psDyn->response.ui16Length & 0xFF);
	pui8Buffer[6] = ((psDyn->response.ui16Length>>8) & 0xFF);
	pui8Buffer[7] = 0x55;//psDyn->response.ui8Instruction;
	pui8Buffer[8] = psDyn->response.ui8Error;
	//payload is already there
	ui16Size = psDyn->response.ui16Length+7;
	ui16Crc = update_crc(0, pui8Buffer, ui16Size-2);
	pui8Buffer[ui16Size-2] = ui16Crc&0xFF;
	pui8Buffer[ui16Size-1] = (ui16Crc>>8)&0xFF;
	return ui16Size;
}

bool setValue(uint16_t ui16ID,uint32_t ui32Value)
{
	uint16_t ui16Idx;
	for (ui16Idx = 0; ui16Idx < DYN_MAX_ELEMENTS; ui16Idx++)
	{
		if (elements[ui16Idx][0] == ui16ID)
		{
			if (elements[ui16Idx][1] == 1)
			{
				dynBuffer[ui16ID] = (uint8_t)(ui32Value & 0xFF);
				return true;
			}
			else if (elements[ui16Idx][1] == 2)
			{
				dynBuffer[ui16ID] = (uint8_t)(ui32Value & 0xFF);
				dynBuffer[ui16ID+1] = (uint8_t)((ui32Value>>8) & 0xFF);
				return true;
			}
			else if (elements[ui16Idx][1] == 4)
			{
				dynBuffer[ui16ID] = (uint8_t)(ui32Value & 0xFF);
				dynBuffer[ui16ID+1] = (uint8_t)((ui32Value>>8) & 0xFF);
				dynBuffer[ui16ID+2] = (uint8_t)((ui32Value>>16) & 0xFF);
				dynBuffer[ui16ID+4] = (uint8_t)((ui32Value>>24) & 0xFF);
				return true;
			}
			else
			{
				return false;
			}
		}
	}
	return false;
}

bool getValue(uint16_t ui16ID,uint32_t *pui32Value)
{
	uint16_t ui16Idx;
	for (ui16Idx = 0; ui16Idx < DYN_MAX_ELEMENTS; ui16Idx++)
	{
		if (elements[ui16Idx][0] == ui16ID)
		{
			if (elements[ui16Idx][1] == 1)
			{
				*pui32Value = (uint32_t)dynBuffer[ui16ID];
				return true;
			}
			else if (elements[ui16Idx][1] == 2)
			{
				*pui32Value = (uint32_t)(dynBuffer[ui16ID] + (dynBuffer[ui16ID+1]<<8) );
				return true;
			}
			else if (elements[ui16Idx][1] == 4)
			{
				*pui32Value = (uint32_t)(dynBuffer[ui16ID] + (dynBuffer[ui16ID+1]<<8) + (dynBuffer[ui16ID+2]<<16) + (dynBuffer[ui16ID+3]<<24) );
				return true;
			}
			else
			{
				return false;
			}
		}
	}
	return false;
}

bool dynamixelInit(dyn_t *psDyn, uint8_t ui8Id)
{
	psDyn->ui8Id = ui8Id;
	//
	dynBuffer[0] = 0x06; //Fake XM430 W210
	dynBuffer[1] = 0x04;
	dynBuffer[2] = 0x26;
	setValue(Model_Number, 1080);
	setValue(Model_Information, ui8Id);
	setValue(Firmware_Version, 38);
	setValue(ID, ui8Id);
	setValue(Baud_Rate, 1);
	setValue(Return_Delay_Time, 250);
	setValue(Drive_Mode, 0);
	setValue(Operating_Mode, 3);
	setValue(Secondary_Shadow__ID, 255);
	setValue(Protocol_Type, 2);
	setValue(Homing_Offset, 0);
	setValue(Moving_Threshold, 10);
	setValue(Temperature_Limit, 80);
	setValue(Max_Voltage_Limit, 150);
	setValue(Min_Voltage_Limit, 100);
	setValue(PWM_Limit, 855);
	setValue(Velocity_Limit, 1023);
	setValue(Max_Position_Limit, 3584);
	setValue(Min_Position_Limit, 512);
	setValue(Startup_Configuration, 0);
	setValue(Shutdown, 52);
	setValue(Torque_Enable, 0);
	setValue(LED, 0);
	setValue(Status_Return_Level, 2);
	setValue(Registered_Instruction, 0);
	setValue(Hardware_Error_Status, 0);
	setValue(Velocity_I_Gain, 1920);
	setValue(Velocity_P_Gain, 100);
	setValue(Position_D_Gain, 0);
	setValue(Position_I_Gain, 0);
	setValue(Position_P_Gain, 700);
	setValue(Feedforward_2nd_Gain, 0);
	setValue(Feedforward_1st_Gain, 0);
	setValue(Bus_Watchdog, 0);
	setValue(Goal_PWM, 0);
	setValue(Goal_Velocity, 0);
	setValue(Profile_Acceleration, 0);
	setValue(Profile_Velocity, 0);
	setValue(Goal_Position, 2048);
	setValue(Realtime_Tick, 0);
	setValue(Moving, 0);
	setValue(Moving_Status, 1);
	setValue(Present_PWM, 0);
	setValue(Present_Load, 200);
	setValue(Present_Velocity, 0);
	setValue(Present_Position, 1024);
	setValue(Velocity_Trajectory, 0);
	setValue(Position_Trajectory, 0);
	setValue(Present_Input_Voltage, 120);
	setValue(Present_Temperature, 25);



}
