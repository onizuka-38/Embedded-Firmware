#ifndef TINYML_INFERENCE_H
#define TINYML_INFERENCE_H

#include <stdint.h>

int tinyml_predict_label(const float *features, uint32_t feature_count);

#endif
