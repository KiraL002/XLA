"""Khai báo nhánh OpenCV tham chiếu, tách khỏi thuật toán chính.

Mỗi người bổ sung hàm tương ứng theo lượt ghép, không cùng sửa tệp một lúc.
Chỉ nhập cv2 khi gọi hàm tham chiếu để các module chính có thể chạy độc lập.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from pipeline import PipelineResult


def reference_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Kiệt: cvtColor COLOR_RGB2GRAY trên float32 để giữ phần thập phân."""
    if not isinstance(rgb, np.ndarray) or rgb.dtype != np.uint8:
        raise ValueError("Ảnh RGB phải là mảng NumPy uint8.")
    if rgb.ndim != 3 or rgb.shape[2] != 3 or min(rgb.shape[:2]) == 0:
        raise ValueError("Ảnh RGB phải có dạng (H, W, 3) với H, W dương.")
    import cv2

    return cv2.cvtColor(rgb.astype(np.float32), cv2.COLOR_RGB2GRAY)


def reference_mean_filter(
    gray: NDArray[np.float32], ksize: int = 3
) -> NDArray[np.float32]:
    """Hiếu: lọc trung bình OpenCV với cùng ksize và BORDER_REPLICATE."""
    raise NotImplementedError("Hiếu phụ trách phần tham chiếu bộ lọc.")


def reference_sobel_magnitude(gray: NDArray[np.float32]) -> NDArray[np.float32]:
    """Long: Sobel OpenCV CV_32F, kernel 3×3, BORDER_REPLICATE."""
    raise NotImplementedError("Long phụ trách phần tham chiếu Sobel.")


def run_reference_pipeline(
    rgb: NDArray[np.uint8], ksize: int = 3, threshold: float = 100.0
) -> PipelineResult:
    """Long tích hợp nhánh tham chiếu; giữ cùng quy tắc phân ngưỡng và tạo tranh.

    Ghi rõ sai khác mức xám nếu dùng cv2.cvtColor. Đối chiếu riêng các bộ lọc
    phải dùng cùng một ảnh xám để sai số mức xám không lan sang bước sau.
    """
    raise NotImplementedError("Cả nhóm ghép nhánh tham chiếu sau khi hoàn thành từng hàm.")
