"""Phân ngưỡng và tạo tranh nét bằng NumPy. Phụ trách: Kiệt."""

from __future__ import annotations

import math
from numbers import Real

import numpy as np
from numpy.typing import NDArray


def threshold_edges(
    magnitude: NDArray[np.float32], threshold: float = 100.0
) -> NDArray[np.bool_]:
    """Trả mặt nạ (H, W), bool theo quy tắc magnitude > threshold.

    magnitude là độ lớn gradient thô float32, hữu hạn, không âm.
    threshold là số hữu hạn không âm. Giá trị đúng bằng ngưỡng không là biên.
    Không sửa đầu vào; dữ liệu sai phải báo ValueError khi triển khai.
    """
    if not isinstance(magnitude, np.ndarray) or magnitude.dtype != np.float32:
        raise ValueError("Độ lớn gradient phải là mảng NumPy float32.")
    if magnitude.ndim != 2 or magnitude.size == 0:
        raise ValueError("Độ lớn gradient phải có dạng (H, W) với H, W dương.")
    if not np.isfinite(magnitude).all() or (magnitude < 0).any():
        raise ValueError("Độ lớn gradient phải hữu hạn và không âm.")
    if isinstance(threshold, (bool, np.bool_)) or not isinstance(threshold, Real):
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.")
    try:
        value = float(threshold)
    except (ValueError, OverflowError) as exc:
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.") from exc
    if not math.isfinite(value) or value < 0:
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.")

    # So sánh gradient thô; giữ độ chính xác của ngưỡng do người dùng nhập.
    return magnitude > np.float64(value)


def render_sketch(edges: NDArray[np.bool_]) -> NDArray[np.uint8]:
    """Đổi mặt nạ bool (H, W) thành tranh uint8 cùng kích thước.

    Điểm True trở thành nét đen 0; False trở thành nền trắng 255.
    Không sửa edges; dữ liệu sai phải báo ValueError khi triển khai.
    """
    if not isinstance(edges, np.ndarray) or edges.dtype != np.bool_:
        raise ValueError("Mặt nạ biên phải là mảng NumPy bool.")
    if edges.ndim != 2 or edges.size == 0:
        raise ValueError("Mặt nạ biên phải có dạng (H, W) với H, W dương.")

    # True là nét đen; các điểm còn lại giữ nền trắng.
    sketch = np.full(edges.shape, 255, dtype=np.uint8)
    sketch[edges] = 0
    return sketch
