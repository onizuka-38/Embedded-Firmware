#include "bms_state.h"

#include <assert.h>
#include <stdint.h>

int main(void)
{
    bms_state_t state;

    const uint8_t frame_180[8] = {0x0E, 0x74, 0xFF, 0x9C, 0U, 0U, 0U, 0U};
    const uint8_t frame_181[8] = {0x03, 0x84, 0x10, 0x70, 0U, 0U, 0U, 0U};
    const uint8_t frame_182[8] = {0x0A, 0x00, 0x1A, 0x00, 0U, 0U, 0U, 0U};

    bms_state_init(&state);

    bms_state_update_from_frame(&state, 0x180U, frame_180, 8U);
    bms_state_update_from_frame(&state, 0x181U, frame_181, 8U);
    bms_state_update_from_frame(&state, 0x182U, frame_182, 8U);

    assert(state.pack_mv == 3700U);
    assert(state.pack_ma < 0);
    assert((state.warning_flags & BMS_WARN_OVERVOLT) != 0U);
    assert((state.warning_flags & BMS_WARN_UNDERVOLT) != 0U);
    assert((state.warning_flags & BMS_WARN_OVERTEMP) != 0U);

    return 0;
}
