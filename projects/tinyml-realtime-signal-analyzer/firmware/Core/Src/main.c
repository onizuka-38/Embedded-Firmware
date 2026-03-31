#include "main.h"

#include "sensor_adapter.h"
#include "telemetry.h"
#include "tinyml_inference.h"

#include "tinyml_model_params.h"

static void normalize_features(float *features)
{
    for (uint32_t i = 0; i < TINYML_FEATURE_COUNT; ++i) {
        features[i] = (features[i] - kTinyMlFeatureMeans[i]) / kTinyMlFeatureStds[i];
    }
}

int main(void)
{
    float features[TINYML_FEATURE_COUNT];
    float probability = 0.0f;
    int32_t label = 0;

    sensor_reset();

#if defined(TINYML_CAPTURE_RAW_STREAM)
    while (1) {
        float raw = 0.0f;
        if (sensor_read_raw_sample(&raw) != 0) {
            continue;
        }
        (void)telemetry_send_sample(raw);
    }
#else
    if (tinyml_init() != TINYML_STATUS_OK) {
        while (1) {
        }
    }

    while (1) {
        const int sensor_status = sensor_read_feature_vector(features, TINYML_FEATURE_COUNT);
        if (sensor_status != 0) {
            continue;
        }

        normalize_features(features);

        if (tinyml_predict(features, TINYML_FEATURE_COUNT, &probability, &label) != TINYML_STATUS_OK) {
            continue;
        }

        (void)telemetry_send_inference(probability, (int)label);
    }
#endif
}

void SystemClock_Config(void)
{
}
