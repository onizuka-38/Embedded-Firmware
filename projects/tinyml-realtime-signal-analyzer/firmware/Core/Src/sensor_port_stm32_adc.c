#include "sensor_port.h"

#include <stdint.h>

#if defined(USE_STM32_ADC_SENSOR)
#include "adc.h"

int sensor_port_read_sample(float *out_sample)
{
    uint32_t raw = 0U;

    if (out_sample == 0) {
        return -1;
    }

    if (HAL_ADC_Start(&hadc1) != HAL_OK) {
        return -2;
    }
    if (HAL_ADC_PollForConversion(&hadc1, 5U) != HAL_OK) {
        (void)HAL_ADC_Stop(&hadc1);
        return -3;
    }

    raw = HAL_ADC_GetValue(&hadc1);
    (void)HAL_ADC_Stop(&hadc1);

    *out_sample = (((float)raw / 4095.0f) * 2.0f) - 1.0f;
    return 0;
}

#endif
