#ifndef SIGNAL_FEATURES_H
#define SIGNAL_FEATURES_H

#include <stdint.h>

#define SIGNAL_FEATURE_COUNT (6U)

int signal_extract_features(
    const float *window,
    uint32_t window_size,
    float *out_features,
    uint32_t feature_count);

#endif
