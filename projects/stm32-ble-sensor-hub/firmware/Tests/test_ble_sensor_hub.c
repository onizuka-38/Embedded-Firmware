#include "ble_link.h"
#include "sensor_hub.h"

#include <assert.h>
#include <stdint.h>

int main(void)
{
    sensor_snapshot_t snapshot;
    const uint8_t* payload;

    sensor_hub_init();
    ble_link_init();

    assert(sensor_hub_poll(&snapshot) == SENSOR_STATUS_OK);
    assert(snapshot.valid == 1U);
    assert(ble_link_publish(&snapshot) == 0);

    payload = ble_link_last_payload();
    assert(payload[0] == 0xA5U);

    {
        uint8_t checksum = 0U;
        for (uint8_t i = 0U; i < 11U; ++i) {
            checksum ^= payload[i];
        }
        assert(checksum == payload[11]);
    }

    return 0;
}
