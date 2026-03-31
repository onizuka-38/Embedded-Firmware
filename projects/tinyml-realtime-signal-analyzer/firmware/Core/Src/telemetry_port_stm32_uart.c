#include "telemetry_port.h"

#if defined(USE_STM32_UART_TELEMETRY)

#include "usart.h"

int telemetry_port_send_line(const char *line, uint32_t length)
{
    if (line == 0 || length == 0U) {
        return -1;
    }

    if (HAL_UART_Transmit(&huart2, (uint8_t *)line, (uint16_t)length, 20U) != HAL_OK) {
        return -2;
    }
    return 0;
}

#endif
