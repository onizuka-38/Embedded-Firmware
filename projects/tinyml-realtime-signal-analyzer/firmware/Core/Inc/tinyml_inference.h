#ifndef TINYML_INFERENCE_H
#define TINYML_INFERENCE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum tinyml_status_t {
    TINYML_STATUS_OK = 0,
    TINYML_STATUS_ERROR = -1,
    TINYML_STATUS_INVALID_ARG = -2,
    TINYML_STATUS_NOT_READY = -3
} tinyml_status_t;

tinyml_status_t tinyml_init(void);
tinyml_status_t tinyml_predict(
    const float *features,
    uint32_t feature_count,
    float *probability,
    int32_t *label);

#ifdef __cplusplus
}
#endif

#endif
