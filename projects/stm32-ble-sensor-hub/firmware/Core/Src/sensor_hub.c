#include "sensor_hub.h"

#define SENSOR_WINDOW (8U)
#define SENSOR_STALE_MS (1500U)

static sensor_snapshot_t g_last;
static uint16_t g_adc_hist[SENSOR_WINDOW];
static uint8_t g_hist_idx = 0U;
static uint8_t g_hist_count = 0U;

#if defined(__GNUC__)
__attribute__((weak))
#endif
int sensor_port_read(uint16_t *adc_mv, int16_t *temp_centi, int16_t *humidity_centi)
{
    static uint16_t base = 1200U;
    base = (uint16_t)(base + 1U);
    *adc_mv = base;
    *temp_centi = 2510;
    *humidity_centi = 5000;
    return 0;
}

#if defined(__GNUC__)
__attribute__((weak))
#endif
uint32_t sensor_port_millis(void)
{
    static uint32_t ms = 0U;
    ms += 100U;
    return ms;
}

static uint16_t moving_average_adc(uint16_t value)
{
    uint32_t sum = 0U;

    g_adc_hist[g_hist_idx] = value;
    g_hist_idx = (uint8_t)((g_hist_idx + 1U) % SENSOR_WINDOW);
    if (g_hist_count < SENSOR_WINDOW) {
        g_hist_count += 1U;
    }

    for (uint8_t i = 0U; i < g_hist_count; ++i) {
        sum += g_adc_hist[i];
    }

    return (uint16_t)(sum / g_hist_count);
}

void sensor_hub_init(void)
{
    g_last.adc_mv = 0U;
    g_last.temp_centi = 0;
    g_last.humidity_centi = 0;
    g_last.valid = 0U;
    g_last.timestamp_ms = 0U;
    g_hist_idx = 0U;
    g_hist_count = 0U;
}

sensor_status_t sensor_hub_poll(sensor_snapshot_t *out_snapshot)
{
    uint16_t adc_mv = 0U;
    int16_t temp_centi = 0;
    int16_t humidity_centi = 0;
    uint32_t now_ms;

    if (out_snapshot == 0) {
        return SENSOR_STATUS_ERROR;
    }

    now_ms = sensor_port_millis();

    if (sensor_port_read(&adc_mv, &temp_centi, &humidity_centi) == 0) {
        g_last.adc_mv = moving_average_adc(adc_mv);
        g_last.temp_centi = temp_centi;
        g_last.humidity_centi = humidity_centi;
        g_last.valid = 1U;
        g_last.timestamp_ms = now_ms;
        *out_snapshot = g_last;
        return SENSOR_STATUS_OK;
    }

    if (g_last.valid == 1U && (now_ms - g_last.timestamp_ms) <= SENSOR_STALE_MS) {
        *out_snapshot = g_last;
        return SENSOR_STATUS_STALE;
    }

    g_last.valid = 0U;
    *out_snapshot = g_last;
    return SENSOR_STATUS_ERROR;
}
