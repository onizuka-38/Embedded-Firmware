#include "sensor_adapter.h"

#include "sensor_port.h"
#include "signal_features.h"

#include <stdint.h>

#define SENSOR_WINDOW_SIZE (128U)

static float g_ring[SENSOR_WINDOW_SIZE];
static uint32_t g_count = 0U;
static uint32_t g_head = 0U;

void sensor_reset(void)
{
    g_count = 0U;
    g_head = 0U;
}

int sensor_push_sample(float sample)
{
    g_ring[g_head] = sample;
    g_head = (g_head + 1U) % SENSOR_WINDOW_SIZE;
    if (g_count < SENSOR_WINDOW_SIZE) {
        g_count += 1U;
    }
    return 0;
}

static int sensor_build_window(float *window_out)
{
    if (g_count < SENSOR_WINDOW_SIZE) {
        return -1;
    }

    uint32_t idx = g_head;
    for (uint32_t i = 0; i < SENSOR_WINDOW_SIZE; ++i) {
        window_out[i] = g_ring[idx];
        idx = (idx + 1U) % SENSOR_WINDOW_SIZE;
    }
    return 0;
}

int sensor_read_feature_vector(float *features, uint32_t feature_count)
{
    float sample = 0.0f;
    float window[SENSOR_WINDOW_SIZE];

    if (features == 0) {
        return -1;
    }
    if (feature_count != SIGNAL_FEATURE_COUNT) {
        return -1;
    }

    if (sensor_port_read_sample(&sample) != 0) {
        return -1;
    }

    sensor_push_sample(sample);

    if (sensor_build_window(window) != 0) {
        return -2;
    }

    return signal_extract_features(window, SENSOR_WINDOW_SIZE, features, feature_count);
}
