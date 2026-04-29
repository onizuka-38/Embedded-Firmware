from __future__ import annotations


def clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


class PID:
    def __init__(self, kp: float, ki: float, kd: float, out_min: float, out_max: float) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.out_min = out_min
        self.out_max = out_max
        self.i_term = 0.0
        self.prev_error = 0.0

    def step(self, target: float, measured: float, dt_s: float) -> float:
        if dt_s <= 0.0:
            return 0.0
        error = target - measured
        p = self.kp * error
        d = self.kd * (error - self.prev_error) / dt_s

        self.i_term += self.ki * error * dt_s
        self.i_term = clamp(self.i_term, self.out_min, self.out_max)

        raw = p + self.i_term + d
        out = clamp(raw, self.out_min, self.out_max)
        if out != raw:
            self.i_term -= self.ki * error * dt_s
            self.i_term = clamp(self.i_term, self.out_min, self.out_max)

        self.prev_error = error
        return out
