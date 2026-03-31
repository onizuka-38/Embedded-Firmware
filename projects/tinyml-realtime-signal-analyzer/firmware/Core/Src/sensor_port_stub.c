#include "sensor_port.h"

#include <stdint.h>

int sensor_port_read_sample(float *out_sample)
{
    static uint32_t tick = 0U;
    const float phase = (float)(tick % 32U) / 31.0f;
    float sample = (phase * 2.0f) - 1.0f;

    if (((tick / 256U) % 2U) == 1U) {
        sample *= 1.8f;
    }

    if (out_sample == 0) {
        return -1;
    }

    *out_sample = sample;
    tick += 1U;
    return 0;
}
