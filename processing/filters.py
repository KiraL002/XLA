"""Bộ lọc trung bình và trung vị tự cài đặt bằng NumPy."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _validate_gray(gray: NDArray[np.float32]) -> None:
    if not isinstance(gray, np.ndarray):
        raise ValueError("gray phải là một mảng NumPy.")
    if gray.ndim != 2 or gray.shape[0] <= 0 or gray.shape[1] <= 0:
        raise ValueError("gray phải có dạng (H, W), với H và W lớn hơn 0.")
    if gray.dtype != np.float32:
        raise ValueError("gray phải có kiểu dữ liệu float32.")
    if not np.isfinite(gray).all():
        raise ValueError("gray chỉ được chứa các giá trị hữu hạn.")
    if np.any((gray < 0.0) | (gray > 255.0)):
        raise ValueError("Các giá trị trong gray phải nằm trong [0, 255].")


def mean_filter(gray: NDArray[np.float32], ksize: int = 3) -> NDArray[np.float32]:
    """Lọc trung bình 3×3 hoặc 5×5 trên ảnh xám float32, bù rìa bằng lặp pixel."""
    _validate_gray(gray)
    if isinstance(ksize, (bool, np.bool_)) or not isinstance(ksize, (int, np.integer)):
        raise ValueError("ksize phải là số nguyên 3 hoặc 5.")
    if ksize not in (3, 5):
        raise ValueError("ksize chỉ nhận giá trị 3 hoặc 5.")

    # Bù rìa bằng cách lặp lại pixel gần nhất; không thay đổi mảng đầu vào.
    radius = ksize // 2
    padded = np.pad(gray, ((radius, radius), (radius, radius)), mode="edge")
    total = np.zeros(gray.shape, dtype=np.float32)

    # Tính tổng từng vùng ksize×ksize bằng NumPy, không gọi bộ lọc dựng sẵn.
    height, width = gray.shape
    for row_offset in range(ksize):
        for col_offset in range(ksize):
            total += padded[
                row_offset : row_offset + height,
                col_offset : col_offset + width,
            ]

    total /= np.float32(ksize * ksize)
    return total


def median_filter_3x3(gray: NDArray[np.float32]) -> NDArray[np.float32]:
    """Lấy trung vị của 9 pixel quanh mỗi điểm để giảm nhiễu xung."""
    _validate_gray(gray)
    padded = np.pad(gray, 1, mode="edge")
    windows = np.lib.stride_tricks.sliding_window_view(padded, (3, 3))
    result = np.empty_like(gray)
    # Tính theo dải hàng để giới hạn mảng tạm trên ảnh độ phân giải cao.
    for start in range(0, gray.shape[0], 128):
        rows = slice(start, start + 128)
        result[rows] = np.median(windows[rows], axis=(-2, -1))
    return result
