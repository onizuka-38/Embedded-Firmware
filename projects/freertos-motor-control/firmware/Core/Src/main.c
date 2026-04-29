#include "motor_control.h"

int main(void)
{
    motor_control_init();
    motor_control_set_target_rps(15.0f);

    while (1) {
        motor_control_update_feedback(12.0f);
        motor_control_step(0.001f);
    }
}
