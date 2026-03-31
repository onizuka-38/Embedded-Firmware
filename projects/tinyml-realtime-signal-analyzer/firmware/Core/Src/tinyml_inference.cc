#include "tinyml_inference.h"

#include "tinyml_model_data.h"

#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#define TINYML_TENSOR_ARENA_BYTES (24 * 1024)

namespace {

tflite::MicroErrorReporter g_micro_error_reporter;
tflite::ErrorReporter* g_error_reporter = &g_micro_error_reporter;
const tflite::Model* g_model = nullptr;
TfLiteTensor* g_input_tensor = nullptr;
TfLiteTensor* g_output_tensor = nullptr;
uint8_t g_tensor_arena[TINYML_TENSOR_ARENA_BYTES];

using Resolver = tflite::MicroMutableOpResolver<8>;
Resolver g_resolver;
tflite::MicroInterpreter* g_interpreter = nullptr;

}  // namespace

extern "C" tinyml_status_t tinyml_init(void)
{
    g_model = tflite::GetModel(g_tinyml_model_data);
    if (g_model == nullptr) {
        return TINYML_STATUS_ERROR;
    }
    if (g_model->version() != TFLITE_SCHEMA_VERSION) {
        return TINYML_STATUS_ERROR;
    }

    if (g_resolver.AddFullyConnected() != kTfLiteOk) {
        return TINYML_STATUS_ERROR;
    }
    if (g_resolver.AddLogistic() != kTfLiteOk) {
        return TINYML_STATUS_ERROR;
    }
    if (g_resolver.AddReshape() != kTfLiteOk) {
        return TINYML_STATUS_ERROR;
    }

    static tflite::MicroInterpreter static_interpreter(
        g_model,
        g_resolver,
        g_tensor_arena,
        TINYML_TENSOR_ARENA_BYTES,
        g_error_reporter);

    g_interpreter = &static_interpreter;
    if (g_interpreter->AllocateTensors() != kTfLiteOk) {
        g_interpreter = nullptr;
        return TINYML_STATUS_ERROR;
    }

    g_input_tensor = g_interpreter->input(0);
    g_output_tensor = g_interpreter->output(0);

    if (g_input_tensor == nullptr || g_output_tensor == nullptr) {
        g_interpreter = nullptr;
        return TINYML_STATUS_ERROR;
    }

    return TINYML_STATUS_OK;
}

extern "C" tinyml_status_t tinyml_predict(
    const float* features,
    uint32_t feature_count,
    float* probability,
    int32_t* label)
{
    if (features == nullptr || probability == nullptr || label == nullptr) {
        return TINYML_STATUS_INVALID_ARG;
    }
    if (g_interpreter == nullptr || g_input_tensor == nullptr || g_output_tensor == nullptr) {
        return TINYML_STATUS_NOT_READY;
    }

    const uint32_t expected_count = (uint32_t)g_input_tensor->bytes / (uint32_t)sizeof(float);
    if (feature_count != expected_count) {
        return TINYML_STATUS_INVALID_ARG;
    }

    for (uint32_t i = 0; i < feature_count; ++i) {
        g_input_tensor->data.f[i] = features[i];
    }

    if (g_interpreter->Invoke() != kTfLiteOk) {
        return TINYML_STATUS_ERROR;
    }

    *probability = g_output_tensor->data.f[0];
    *label = (*probability >= 0.5f) ? 1 : 0;
    return TINYML_STATUS_OK;
}
