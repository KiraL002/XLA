"""Khung bộ lọc trung bình tự cài đặt. Phụ trách: Hiếu."""

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
    raise NotImplementedError("Hiếu phụ trách triển khai mean_filter.")
