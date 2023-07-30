#include "utilis.h"

bool checkPos(int32_t actualPos, int32_t desPos, int32_t threshold)
{
	return ( (desPos < (actualPos + threshold)) && (desPos < (actualPos + threshold)) );
}
