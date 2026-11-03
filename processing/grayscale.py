"""Khung chuyển ảnh RGB thành mức xám. Phụ trách: Kiệt."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def to_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Nhận RGB (H, W, 3), uint8; trả (H, W), float32 trong [0, 255].

    Công thức thống nhất: Y = 0.299R + 0.587G + 0.114B.
    Không làm tròn về uint8 và không sửa mảng đầu vào.
    Dữ liệu sai dạng/kiểu hoặc ảnh rỗng phải báo ValueError khi triển khai.
    """
    raise NotImplementedError("Kiệt phụ trách triển khai to_grayscale.")
