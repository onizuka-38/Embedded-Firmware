#include "ble_link.h"

static uint8_t g_payload[BLE_PAYLOAD_BYTES];

#if defined(__GNUC__)
__attribute__((weak))
#endif
int ble_port_advertise_payload(const uint8_t *payload, uint8_t length)
{
    (void)payload;
    return (length == BLE_PAYLOAD_BYTES) ? 0 : -1;
}

static uint8_t checksum8(const uint8_t *data, uint8_t len)
{
    uint8_t cs = 0U;
    for (uint8_t i = 0U; i < len; ++i) {
        cs ^= data[i];
    }
    return cs;
}

void ble_link_init(void)
{
    for (uint8_t i = 0U; i < BLE_PAYLOAD_BYTES; ++i) {
        g_payload[i] = 0U;
    }
}

int ble_link_publish(const sensor_snapshot_t *snapshot)
{
    if (snapshot == 0 || snapshot->valid == 0U) {
        return -1;
    }

    g_payload[0] = 0xA5U;
    g_payload[1] = (uint8_t)(snapshot->adc_mv >> 8);
    g_payload[2] = (uint8_t)(snapshot->adc_mv & 0xFFU);
    g_payload[3] = (uint8_t)(snapshot->temp_centi >> 8);
    g_payload[4] = (uint8_t)(snapshot->temp_centi & 0xFFU);
    g_payload[5] = (uint8_t)(snapshot->humidity_centi >> 8);
    g_payload[6] = (uint8_t)(snapshot->humidity_centi & 0xFFU);
    g_payload[7] = (uint8_t)(snapshot->timestamp_ms >> 24);
    g_payload[8] = (uint8_t)(snapshot->timestamp_ms >> 16);
    g_payload[9] = (uint8_t)(snapshot->timestamp_ms >> 8);
    g_payload[10] = (uint8_t)(snapshot->timestamp_ms & 0xFFU);
    g_payload[11] = checksum8(g_payload, 11U);

    return ble_port_advertise_payload(g_payload, BLE_PAYLOAD_BYTES);
}

const uint8_t *ble_link_last_payload(void)
{
    return g_payload;
}
