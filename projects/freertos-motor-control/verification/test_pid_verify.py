from __future__ import annotations

from pid_verify import PID


def test_pid_output_clamped() -> None:
    pid = PID(0.8, 0.2, 0.01, 0.0, 1.0)
    out = pid.step(100.0, 0.0, 0.001)
    assert 0.0 <= out <= 1.0


def test_pid_invalid_dt_behavior() -> None:
    pid = PID(0.8, 0.2, 0.01, 0.0, 1.0)
    assert pid.step(10.0, 9.0, 0.0) == 0.0
