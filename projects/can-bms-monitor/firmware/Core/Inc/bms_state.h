#ifndef BMS_STATE_H
#define BMS_STATE_H

#include <stdint.h>

#define BMS_WARN_OVERVOLT (1U << 0)
#define BMS_WARN_UNDERVOLT (1U << 1)
#define BMS_WARN_OVERTEMP (1U << 2)
#define BMS_WARN_CURRENT (1U << 3)

typedef struct bms_state_t {
    uint16_t pack_mv;
    int16_t pack_ma;
    uint16_t soc_tenths;
    uint16_t max_cell_mv;
    uint16_t min_cell_mv;
    int16_t max_temp_centi;
    int16_t min_temp_centi;
    uint8_t warning_flags;
    uint32_t last_update_ms;
} bms_state_t;

void bms_state_init(bms_state_t *state);
void bms_state_update_from_frame(bms_state_t *state, uint32_t can_id, const uint8_t *data, uint8_t len);
void bms_state_apply_rules(bms_state_t *state);

#endif
