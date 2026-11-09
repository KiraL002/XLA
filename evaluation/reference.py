"""Khai báo nhánh OpenCV tham chiếu, tách khỏi thuật toán chính.

Mỗi người bổ sung hàm tương ứng theo lượt ghép, không cùng sửa tệp một lúc.
Chưa gọi hoặc nhập cv2 cho đến khi triển khai phần tham chiếu.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from pipeline import PipelineResult, validate_params, validate_rgb


def reference_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Kiệt: đối chiếu chuyển mức xám bằng OpenCV theo thứ tự RGB."""
    raise NotImplementedError("Kiệt phụ trách phần tham chiếu mức xám.")


def reference_mean_filter(
    gray: NDArray[np.float32], ksize: int = 3
) -> NDArray[np.float32]:
    """Hiếu: lọc trung bình OpenCV với cùng ksize và BORDER_REPLICATE."""
    raise NotImplementedError("Hiếu phụ trách phần tham chiếu bộ lọc.")


def reference_sobel_gradients(
    gray: NDArray[np.float32],
) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """Long: (Gx, Gy) từ cv2.Sobel CV_32F, kernel 3×3, BORDER_REPLICATE.

    Dùng để đối chiếu Gx, Gy trước khi so độ lớn hoặc tranh cuối.
    """
    import cv2  # nhập muộn: chỉ nhánh tham chiếu mới cần OpenCV

    g = np.ascontiguousarray(gray, dtype=np.float32)
    kw = dict(ksize=3, borderType=cv2.BORDER_REPLICATE)
    return (cv2.Sobel(g, cv2.CV_32F, 1, 0, **kw),
            cv2.Sobel(g, cv2.CV_32F, 0, 1, **kw))


def reference_sobel_magnitude(gray: NDArray[np.float32]) -> NDArray[np.float32]:
    """Long: Sobel OpenCV CV_32F, kernel 3×3, BORDER_REPLICATE; trả M thô float32."""
    import cv2

    gx, gy = reference_sobel_gradients(gray)
    return cv2.magnitude(gx, gy)


def run_reference_pipeline(
    rgb: NDArray[np.uint8], ksize: int = 3, threshold: float = 100.0
) -> PipelineResult:
    """Long tích hợp nhánh tham chiếu; giữ cùng quy tắc phân ngưỡng và tạo tranh.

    Ghi rõ sai khác mức xám nếu dùng cv2.cvtColor. Đối chiếu riêng các bộ lọc
    phải dùng cùng một ảnh xám để sai số mức xám không lan sang bước sau.
    """
    from processing.sketch import render_sketch, threshold_edges

    ksize, threshold = validate_params(ksize, threshold)
    validate_rgb(rgb)

    # Các hàm reference_* của Kiệt/Hiếu báo NotImplementedError cho đến khi họ hoàn thành.
    gray = reference_grayscale(rgb)
    smooth = reference_mean_filter(gray, ksize)
    magnitude = reference_sobel_magnitude(smooth)
    # Phân ngưỡng và tạo tranh dùng chung với nhánh chính để chỉ khác ở các bước xử lý ảnh.
    edges = threshold_edges(magnitude, threshold)
    sketch = render_sketch(edges)
    return {
        "gray": gray,
        "smooth": smooth,
        "magnitude": magnitude,
        "edges": edges,
        "sketch": sketch,
    }