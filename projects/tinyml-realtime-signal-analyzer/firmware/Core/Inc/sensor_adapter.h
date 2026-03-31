#ifndef SENSOR_ADAPTER_H
#define SENSOR_ADAPTER_H

#include <stdint.h>

int sensor_read_feature_vector(float *features, uint32_t feature_count);

#endif
