#include "motor_control.h"
#include "pid.h"

#define MOTOR_FAULT_INVALID_DT (1U << 0)
#define MOTOR_FAULT_SPEED_RANGE (1U << 1)
#define MOTOR_MAX_RPS (120.0f)

static pid_state_t g_pid;
static motor_state_t g_state;

static float clamp01(float x)
{
    if (x < 0.0f) {
        return 0.0f;
    }
    if (x > 1.0f) {
        return 1.0f;
    }
    return x;
}

void motor_control_init(void)
{
    pid_init(&g_pid, 0.8f, 0.2f, 0.01f, 0.0f, 1.0f);
    g_state.target_rps = 0.0f;
    g_state.measured_rps = 0.0f;
    g_state.duty = 0.0f;
    g_state.fault_flags = 0U;
}

void motor_control_set_target_rps(float target_rps)
{
    if (target_rps < 0.0f) {
        target_rps = 0.0f;
    }
    if (target_rps > MOTOR_MAX_RPS) {
        target_rps = MOTOR_MAX_RPS;
    }
    g_state.target_rps = target_rps;
}

void motor_control_update_feedback(float measured_rps)
{
    g_state.measured_rps = measured_rps;

    if (measured_rps < -1.0f || measured_rps > (MOTOR_MAX_RPS * 1.2f)) {
        g_state.fault_flags |= MOTOR_FAULT_SPEED_RANGE;
    }
}

void motor_control_step(float dt_s)
{
    if (dt_s <= 0.0f) {
        g_state.fault_flags |= MOTOR_FAULT_INVALID_DT;
        return;
    }

    g_state.duty = clamp01(pid_step(&g_pid, g_state.target_rps, g_state.measured_rps, dt_s));
}

motor_state_t motor_control_get_state(void)
{
    return g_state;
}
