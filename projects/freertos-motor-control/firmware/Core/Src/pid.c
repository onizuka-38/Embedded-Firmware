#include "pid.h"

static float clamp(float x, float lo, float hi)
{
    if (x < lo) {
        return lo;
    }
    if (x > hi) {
        return hi;
    }
    return x;
}

void pid_init(pid_state_t *pid, float kp, float ki, float kd, float out_min, float out_max)
{
    if (pid == 0 || out_min >= out_max) {
        return;
    }

    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->out_min = out_min;
    pid->out_max = out_max;
    pid_reset(pid);
}

void pid_reset(pid_state_t *pid)
{
    if (pid == 0) {
        return;
    }

    pid->i_term = 0.0f;
    pid->prev_error = 0.0f;
}

float pid_step(pid_state_t *pid, float target, float measured, float dt_s)
{
    float error;
    float p;
    float d;
    float out_raw;
    float out;

    if (pid == 0 || dt_s <= 0.0f) {
        return 0.0f;
    }

    error = target - measured;
    p = pid->kp * error;
    d = pid->kd * (error - pid->prev_error) / dt_s;

    pid->i_term += pid->ki * error * dt_s;
    pid->i_term = clamp(pid->i_term, pid->out_min, pid->out_max);

    out_raw = p + pid->i_term + d;
    out = clamp(out_raw, pid->out_min, pid->out_max);

    if (out != out_raw) {
        pid->i_term -= pid->ki * error * dt_s;
        pid->i_term = clamp(pid->i_term, pid->out_min, pid->out_max);
    }

    pid->prev_error = error;
    return out;
}
