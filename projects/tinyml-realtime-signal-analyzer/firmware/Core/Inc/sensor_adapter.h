#ifndef SENSOR_ADAPTER_H
#define SENSOR_ADAPTER_H

#include <stdint.h>

int sensor_push_sample(float sample);
int sensor_read_feature_vector(float *features, uint32_t feature_count);
void sensor_reset(void);

#endif
