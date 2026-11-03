"""Khai báo công cụ đo thời gian. Phụ trách: Hiếu."""

from __future__ import annotations

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
    raise NotImplementedError("Hiếu phụ trách triển khai measure_runtime.")
