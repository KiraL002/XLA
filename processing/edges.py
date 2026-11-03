"""Khung phát hiện biên bằng Sobel tự cài đặt. Phụ trách: Long."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def sobel_magnitude(gray: NDArray[np.float32]) -> NDArray[np.float32]:
    """Nhận ảnh xám (H, W), float32 trong [0, 255]; trả độ lớn gradient.

    Dùng kernel và quy tắc bù rìa tại docs/INTERFACES.md.
    Kết quả float32, không âm, cùng kích thước; chưa chuẩn hóa về [0, 255].
    Không sửa đầu vào và không gọi cv2.Sobel trong phần tự cài đặt.
    Đầu vào sai phải báo ValueError khi triển khai.
    """
    raise NotImplementedError("Long phụ trách triển khai sobel_magnitude.")
