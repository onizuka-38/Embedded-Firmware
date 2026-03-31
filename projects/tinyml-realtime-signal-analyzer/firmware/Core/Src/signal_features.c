#include "signal_features.h"

#include <math.h>

int signal_extract_features(
    const float *window,
    uint32_t window_size,
    float *out_features,
    uint32_t feature_count)
{
    if (window == 0 || out_features == 0) {
        return -1;
    }
    if (window_size < 4U || feature_count != SIGNAL_FEATURE_COUNT) {
        return -1;
    }

    float sum = 0.0f;
    float abs_sum = 0.0f;
    float energy_sum = 0.0f;
    float min_value = window[0];
    float max_value = window[0];
    uint32_t zero_crossings = 0U;

    for (uint32_t i = 0; i < window_size; ++i) {
        const float value = window[i];
        sum += value;
        abs_sum += fabsf(value);
        energy_sum += value * value;

        if (value < min_value) {
            min_value = value;
        }
        if (value > max_value) {
            max_value = value;
        }

        if (i > 0U) {
            const float prev = window[i - 1U];
            if ((prev < 0.0f && value > 0.0f) || (prev > 0.0f && value < 0.0f)) {
                zero_crossings += 1U;
            }
        }
    }

    const float inv_n = 1.0f / (float)window_size;
    const float mean = sum * inv_n;

    float variance_sum = 0.0f;
    for (uint32_t i = 0; i < window_size; ++i) {
        const float diff = window[i] - mean;
        variance_sum += diff * diff;
    }

    out_features[0] = mean;
    out_features[1] = sqrtf(variance_sum * inv_n);
    out_features[2] = energy_sum * inv_n;
    out_features[3] = abs_sum * inv_n;
    out_features[4] = max_value - min_value;
    out_features[5] = (float)zero_crossings * inv_n;
    return 0;
}
