#include "main.h"

#include "sensor_adapter.h"
#include "tinyml_inference.h"

#include "tinyml_model_params.h"

int main(void)
{
    float features[TINYML_FEATURE_COUNT];
    float probability = 0.0f;
    int32_t label = 0;

    if (tinyml_init() != TINYML_STATUS_OK) {
        while (1) {
        }
    }

    while (1) {
        if (sensor_read_feature_vector(features, TINYML_FEATURE_COUNT) != 0) {
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
