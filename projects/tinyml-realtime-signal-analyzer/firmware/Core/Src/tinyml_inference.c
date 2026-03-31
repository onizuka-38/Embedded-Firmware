#include "tinyml_inference.h"

#include "tinyml_model_params.h"

int tinyml_predict_label(const float *features, uint32_t feature_count)
{
    if (features == 0 || feature_count != TINYML_FEATURE_COUNT) {
        return -1;
    }

    float acc = (float)TINYML_BIAS_Q7 * TINYML_WEIGHT_SCALE;
    for (uint32_t i = 0; i < feature_count; ++i) {
        const float centered = (features[i] - kTinyMlFeatureMeans[i]) / kTinyMlFeatureStds[i];
        acc += centered * ((float)kTinyMlWeightsQ7[i] * TINYML_WEIGHT_SCALE);
    }

    return (acc >= 0.0f) ? 1 : 0;
}
