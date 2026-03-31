#include "sensor_adapter.h"

#include <stdint.h>

int sensor_read_feature_vector(float *features, uint32_t feature_count)
{
    if (features == 0 || feature_count == 0U) {
        return -1;
    }

    for (uint32_t i = 0; i < feature_count; ++i) {
        features[i] = 0.0f;
    }

    return 0;
}
