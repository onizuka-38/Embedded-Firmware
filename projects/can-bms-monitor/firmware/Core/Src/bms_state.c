#include "bms_state.h"

#define CELL_OVERVOLT_MV (4200U)
#define CELL_UNDERVOLT_MV (2900U)
#define TEMP_OVERTEMP_CENTI (6500)
#define CURRENT_LIMIT_MA (30000)

static uint16_t u16be(const uint8_t *data)
{
    return (uint16_t)(((uint16_t)data[0] << 8) | data[1]);
}

static int16_t s16be(const uint8_t *data)
{
    return (int16_t)(((uint16_t)data[0] << 8) | data[1]);
}

void bms_state_init(bms_state_t *state)
{
    if (state == 0) {
        return;
    }

    state->pack_mv = 0U;
    state->pack_ma = 0;
    state->soc_tenths = 0U;
    state->max_cell_mv = 0U;
    state->min_cell_mv = 0U;
    state->max_temp_centi = 0;
    state->min_temp_centi = 0;
    state->warning_flags = 0U;
    state->last_update_ms = 0U;
}

void bms_state_update_from_frame(bms_state_t *state, uint32_t can_id, const uint8_t *data, uint8_t len)
{
    if (state == 0 || data == 0 || len < 4U) {
        return;
    }

    if (can_id == 0x180U) {
        state->pack_mv = u16be(&data[0]);
        state->pack_ma = s16be(&data[2]);
    } else if (can_id == 0x181U) {
        state->soc_tenths = u16be(&data[0]);
        state->max_cell_mv = u16be(&data[2]);
    } else if (can_id == 0x182U) {
        state->min_cell_mv = u16be(&data[0]);
        state->max_temp_centi = s16be(&data[2]);
    } else if (can_id == 0x183U) {
        state->min_temp_centi = s16be(&data[0]);
        state->last_update_ms = (uint32_t)u16be(&data[2]) * 100U;
    }

    bms_state_apply_rules(state);
}

void bms_state_apply_rules(bms_state_t *state)
{
    uint8_t flags = 0U;

    if (state == 0) {
        return;
    }

    if (state->max_cell_mv > CELL_OVERVOLT_MV) {
        flags |= BMS_WARN_OVERVOLT;
    }
    if (state->min_cell_mv > 0U && state->min_cell_mv < CELL_UNDERVOLT_MV) {
        flags |= BMS_WARN_UNDERVOLT;
    }
    if (state->max_temp_centi > TEMP_OVERTEMP_CENTI) {
        flags |= BMS_WARN_OVERTEMP;
    }
    if (state->pack_ma > CURRENT_LIMIT_MA || state->pack_ma < -CURRENT_LIMIT_MA) {
        flags |= BMS_WARN_CURRENT;
    }

    state->warning_flags = flags;
}
