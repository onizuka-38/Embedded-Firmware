#include "motor_control.h"

#include <assert.h>

int main(void)
{
    motor_state_t state;

    motor_control_init();
    motor_control_set_target_rps(20.0f);
    motor_control_update_feedback(10.0f);
    motor_control_step(0.001f);

    state = motor_control_get_state();
    assert(state.duty >= 0.0f);
    assert(state.duty <= 1.0f);

    motor_control_step(0.0f);
    state = motor_control_get_state();
    assert((state.fault_flags & 1U) != 0U);

    motor_control_update_feedback(1000.0f);
    state = motor_control_get_state();
    assert((state.fault_flags & 2U) != 0U);

    return 0;
}
