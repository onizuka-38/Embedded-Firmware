#ifndef SENSOR_HUB_H
#define SENSOR_HUB_H

#include <stdint.h>

typedef enum sensor_status_t {
    SENSOR_STATUS_OK = 0,
    SENSOR_STATUS_STALE = 1,
    SENSOR_STATUS_ERROR = -1
} sensor_status_t;

typedef struct sensor_snapshot_t {
    uint16_t adc_mv;
    int16_t temp_centi;
    int16_t humidity_centi;
    uint8_t valid;
    uint32_t timestamp_ms;
} sensor_snapshot_t;

void sensor_hub_init(void);
sensor_status_t sensor_hub_poll(sensor_snapshot_t *out_snapshot);

#endif
