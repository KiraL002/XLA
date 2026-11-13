"""Công cụ đo thời gian chạy thuật toán. Phụ trách: Hiếu."""

from __future__ import annotations

import statistics
import time
from typing import Callable


def measure_runtime(
    function: Callable[[], object], repeats: int = 5, warmup: int = 1
) -> dict[str, float]:
    """Đo callable không tham số bằng time.perf_counter sau khi triển khai.

    Đơn vị ms; trả các khóa median_ms, min_ms và max_ms.
    repeats là số nguyên >= 5; warmup là số nguyên >= 1.
    Chỉ đo thuật toán, không gộp đọc/lưu tệp hoặc cập nhật giao diện.
    Không tạo số liệu khi chưa gọi và đo function thực tế.
    """
    if not callable(function):
        raise ValueError("function phải là callable không tham số.")
    if isinstance(repeats, bool) or not isinstance(repeats, int) or repeats < 5:
        raise ValueError("repeats phải là số nguyên từ 5 trở lên.")
    if isinstance(warmup, bool) or not isinstance(warmup, int) or warmup < 1:
        raise ValueError("warmup phải là số nguyên từ 1 trở lên.")

    for _ in range(warmup):
        function()

    durations_ms: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        durations_ms.append((time.perf_counter() - start) * 1000.0)

    return {
        "median_ms": statistics.median(durations_ms),
        "min_ms": min(durations_ms),
        "max_ms": max(durations_ms),
    }
