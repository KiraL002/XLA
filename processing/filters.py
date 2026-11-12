"""Bộ lọc trung bình tự cài đặt. Phụ trách: Hiếu."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def mean_filter(gray: NDArray[np.float32], ksize: int = 3) -> NDArray[np.float32]:
    """Làm mịn ảnh xám bằng trung bình vùng ksize×ksize.

    Nhận/trả (H, W), float32, giá trị hữu hạn trong [0, 255].
    Chỉ nhận ksize là số nguyên 3 hoặc 5. Bù rìa bằng mode='edge'.
    Giữ kích thước, không sửa gray, không gọi bộ lọc có sẵn của thư viện.
    Đầu vào sai phải báo ValueError khi triển khai.
    """
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
