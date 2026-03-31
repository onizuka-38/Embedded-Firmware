#include "telemetry.h"

#include "telemetry_port.h"

#include <stdio.h>

int telemetry_send_sample(float sample)
{
    char line[40];
    const int length = snprintf(line, sizeof(line), "RAW,%.6f\n", sample);
    if (length <= 0) {
        return -1;
    }

    return telemetry_port_send_line(line, (uint32_t)length);
}

int telemetry_send_inference(float probability, int label)
{
    char line[56];
    const int length = snprintf(line, sizeof(line), "INF,%.5f,%d\n", probability, label);
    if (length <= 0) {
        return -1;
    }

    return telemetry_port_send_line(line, (uint32_t)length);
}
