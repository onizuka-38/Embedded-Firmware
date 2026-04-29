#include "bms_state.h"

int main(void)
{
    bms_state_t state;
    const uint8_t frame_180[8] = {0x0E, 0x74, 0x00, 0x64, 0U, 0U, 0U, 0U};
    const uint8_t frame_181[8] = {0x03, 0x84, 0x10, 0x36, 0U, 0U, 0U, 0U};
    const uint8_t frame_182[8] = {0x0F, 0xA0, 0x19, 0x64, 0U, 0U, 0U, 0U};

    bms_state_init(&state);

    while (1) {
        bms_state_update_from_frame(&state, 0x180U, frame_180, 8U);
        bms_state_update_from_frame(&state, 0x181U, frame_181, 8U);
        bms_state_update_from_frame(&state, 0x182U, frame_182, 8U);
    }
}
