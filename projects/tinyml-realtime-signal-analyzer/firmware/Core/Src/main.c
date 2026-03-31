#include "main.h"

#include "sensor_adapter.h"
#include "tinyml_inference.h"

#include "tinyml_model_params.h"

int main(void)
{
    float features[TINYML_FEATURE_COUNT];
    float probability = 0.0f;
    int32_t label = 0;

    sensor_reset();

    if (tinyml_init() != TINYML_STATUS_OK) {
        while (1) {
        }
    }

    while (1) {
        const int sensor_status = sensor_read_feature_vector(features, TINYML_FEATURE_COUNT);
        if (sensor_status != 0) {
            continue;
        }

        if (tinyml_predict(features, TINYML_FEATURE_COUNT, &probability, &label) != TINYML_STATUS_OK) {
            continue;
        }

        (void)probability;
        (void)label;
    }
}

void SystemClock_Config(void)
{
}
