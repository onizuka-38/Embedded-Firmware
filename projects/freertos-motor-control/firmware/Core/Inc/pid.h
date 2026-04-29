#ifndef PID_H
#define PID_H

typedef struct pid_state_t {
    float kp;
    float ki;
    float kd;
    float i_term;
    float prev_error;
    float out_min;
    float out_max;
} pid_state_t;

void pid_init(pid_state_t *pid, float kp, float ki, float kd, float out_min, float out_max);
void pid_reset(pid_state_t *pid);
float pid_step(pid_state_t *pid, float target, float measured, float dt_s);

#endif
