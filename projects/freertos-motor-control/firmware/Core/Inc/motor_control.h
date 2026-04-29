#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

typedef struct motor_state_t {
    float target_rps;
    float measured_rps;
    float duty;
    unsigned int fault_flags;
} motor_state_t;

void motor_control_init(void);
void motor_control_set_target_rps(float target_rps);
void motor_control_update_feedback(float measured_rps);
void motor_control_step(float dt_s);
motor_state_t motor_control_get_state(void);

#endif
