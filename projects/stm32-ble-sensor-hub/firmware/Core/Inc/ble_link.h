#ifndef BLE_LINK_H
#define BLE_LINK_H

#include "sensor_hub.h"
#include <stdint.h>

#define BLE_PAYLOAD_BYTES (12U)

void ble_link_init(void);
int ble_link_publish(const sensor_snapshot_t *snapshot);
const uint8_t *ble_link_last_payload(void);

#endif
