#include "ble_link.h"
#include "sensor_hub.h"

int main(void)
{
    sensor_snapshot_t snapshot;

    sensor_hub_init();
    ble_link_init();

    while (1) {
        sensor_status_t status = sensor_hub_poll(&snapshot);
        if (status == SENSOR_STATUS_OK || status == SENSOR_STATUS_STALE) {
            (void)ble_link_publish(&snapshot);
        }
    }
}
