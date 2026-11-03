"""Khung phân ngưỡng và tạo tranh nét. Phụ trách: Kiệt."""

from __future__ import annotations

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
    raise NotImplementedError("Kiệt phụ trách triển khai threshold_edges.")


def render_sketch(edges: NDArray[np.bool_]) -> NDArray[np.uint8]:
    """Đổi mặt nạ bool (H, W) thành tranh uint8 cùng kích thước.

    Điểm True trở thành nét đen 0; False trở thành nền trắng 255.
    Không sửa edges; dữ liệu sai phải báo ValueError khi triển khai.
    """
    raise NotImplementedError("Kiệt phụ trách triển khai render_sketch.")
