#include "tinyml_inference.h"

#include "tinyml_model_data.h"

#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#include <math.h>
#include <stdint.h>

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

uint32_t tensor_element_count(const TfLiteTensor* tensor)
{
    if (tensor == nullptr) {
        return 0U;
    }

    switch (tensor->type) {
        case kTfLiteFloat32:
            return (uint32_t)tensor->bytes / (uint32_t)sizeof(float);
        case kTfLiteInt8:
            return (uint32_t)tensor->bytes / (uint32_t)sizeof(int8_t);
        default:
            return 0U;
    }
}

float clamp01(float value)
{
    if (value < 0.0f) {
        return 0.0f;
    }
    if (value > 1.0f) {
        return 1.0f;
    }
    return value;
}

int8_t quantize_to_int8(float value, TfLiteAffineQuantization* quant)
{
    const float scale = quant->scale->data[0];
    const int32_t zero_point = quant->zero_point->data[0];
    const int32_t q = (int32_t)lroundf(value / scale) + zero_point;

    if (q < -128) {
        return -128;
    }
    if (q > 127) {
        return 127;
    }
    return (int8_t)q;
}

float dequantize_int8(int8_t value, TfLiteAffineQuantization* quant)
{
    const float scale = quant->scale->data[0];
    const int32_t zero_point = quant->zero_point->data[0];
    return ((float)value - (float)zero_point) * scale;
}

bool prepare_input(const float* features, uint32_t feature_count)
{
    if (g_input_tensor->type == kTfLiteFloat32) {
        for (uint32_t i = 0; i < feature_count; ++i) {
            g_input_tensor->data.f[i] = features[i];
        }
        return true;
    }

    if (g_input_tensor->type == kTfLiteInt8) {
        if (g_input_tensor->quantization.type != kTfLiteAffineQuantization) {
            return false;
        }

        auto* quant = (TfLiteAffineQuantization*)g_input_tensor->quantization.params;
        if (quant == nullptr || quant->scale == nullptr || quant->zero_point == nullptr) {
            return false;
        }

        for (uint32_t i = 0; i < feature_count; ++i) {
            g_input_tensor->data.int8[i] = quantize_to_int8(features[i], quant);
        }
        return true;
    }

    return false;
}

bool read_output_probability(float* probability)
{
    if (g_output_tensor->type == kTfLiteFloat32) {
        *probability = clamp01(g_output_tensor->data.f[0]);
        return true;
    }

    if (g_output_tensor->type == kTfLiteInt8) {
        if (g_output_tensor->quantization.type != kTfLiteAffineQuantization) {
            return false;
        }

        auto* quant = (TfLiteAffineQuantization*)g_output_tensor->quantization.params;
        if (quant == nullptr || quant->scale == nullptr || quant->zero_point == nullptr) {
            return false;
        }

        *probability = clamp01(dequantize_int8(g_output_tensor->data.int8[0], quant));
        return true;
    }

    return false;
}

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

    const uint32_t expected_count = tensor_element_count(g_input_tensor);
    if (expected_count == 0U || feature_count != expected_count) {
        return TINYML_STATUS_INVALID_ARG;
    }

    if (!prepare_input(features, feature_count)) {
        return TINYML_STATUS_ERROR;
    }

    if (g_interpreter->Invoke() != kTfLiteOk) {
        return TINYML_STATUS_ERROR;
    }

    if (!read_output_probability(probability)) {
        return TINYML_STATUS_ERROR;
    }

    *label = (*probability >= 0.5f) ? 1 : 0;
    return TINYML_STATUS_OK;
}
