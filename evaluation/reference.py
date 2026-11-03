"""Khai báo nhánh OpenCV tham chiếu, tách khỏi thuật toán chính.

Mỗi người bổ sung hàm tương ứng theo lượt ghép, không cùng sửa tệp một lúc.
Chưa gọi hoặc nhập cv2 cho đến khi triển khai phần tham chiếu.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from pipeline import PipelineResult


def reference_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Kiệt: đối chiếu chuyển mức xám bằng OpenCV theo thứ tự RGB."""
    raise NotImplementedError("Kiệt phụ trách phần tham chiếu mức xám.")


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
