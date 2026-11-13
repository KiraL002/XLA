"""Chuyển ảnh RGB thành mức xám bằng NumPy. Phụ trách: Kiệt."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def to_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Nhận RGB (H, W, 3), uint8; trả (H, W), float32 trong [0, 255].

    Công thức thống nhất: Y = 0.299R + 0.587G + 0.114B.
    Không làm tròn về uint8 và không sửa mảng đầu vào.
    Dữ liệu sai dạng/kiểu hoặc ảnh rỗng phải báo ValueError khi triển khai.
    """
    if not isinstance(rgb, np.ndarray) or rgb.dtype != np.uint8:
        raise ValueError("Ảnh RGB phải là mảng NumPy có kiểu uint8.")
    if rgb.ndim != 3 or rgb.shape[2] != 3 or min(rgb.shape[:2]) == 0:
        raise ValueError("Ảnh RGB phải có dạng (H, W, 3) với H, W dương.")

    # Chuyển kiểu trước khi tính để giữ phần thập phân và không sửa ảnh gốc.
    pixels = rgb.astype(np.float32)
    return (
        np.float32(0.299) * pixels[:, :, 0]
        + np.float32(0.587) * pixels[:, :, 1]
        + np.float32(0.114) * pixels[:, :, 2]
    )
