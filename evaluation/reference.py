"""Đối chiếu mức xám, lọc trung bình và Sobel bằng OpenCV."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from pipeline import PipelineResult, validate_params, validate_rgb


def reference_grayscale(rgb: NDArray[np.uint8]) -> NDArray[np.float32]:
    """Dùng COLOR_RGB2GRAY trên float32 để giữ phần thập phân."""
    if not isinstance(rgb, np.ndarray) or rgb.dtype != np.uint8:
        raise ValueError("Ảnh RGB phải là mảng NumPy uint8.")
    if rgb.ndim != 3 or rgb.shape[2] != 3 or min(rgb.shape[:2]) == 0:
        raise ValueError("Ảnh RGB phải có dạng (H, W, 3) với H, W dương.")
    import cv2

    return cv2.cvtColor(rgb.astype(np.float32), cv2.COLOR_RGB2GRAY)


def reference_mean_filter(
    gray: NDArray[np.float32], ksize: int = 3
) -> NDArray[np.float32]:
    """Lọc trung bình OpenCV với cùng ksize và BORDER_REPLICATE."""
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

    # Chỉ nạp OpenCV khi gọi nhánh tham chiếu; nhánh NumPy không phụ thuộc cv2.
    import cv2

    return cv2.blur(
        gray,
        (int(ksize), int(ksize)),
        borderType=cv2.BORDER_REPLICATE,
    )


def reference_sobel_gradients(
    gray: NDArray[np.float32],
) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """Tính (Gx, Gy) bằng cv2.Sobel CV_32F, kernel 3×3, BORDER_REPLICATE.

    Dùng để đối chiếu Gx, Gy trước khi so độ lớn hoặc tranh cuối.
    """
    import cv2  # nhập muộn: chỉ nhánh tham chiếu mới cần OpenCV

    g = np.ascontiguousarray(gray, dtype=np.float32)
    kw = dict(ksize=3, borderType=cv2.BORDER_REPLICATE)
    return (cv2.Sobel(g, cv2.CV_32F, 1, 0, **kw),
            cv2.Sobel(g, cv2.CV_32F, 0, 1, **kw))


def reference_sobel_magnitude(gray: NDArray[np.float32]) -> NDArray[np.float32]:
    """Tính độ lớn Sobel thô bằng OpenCV, kiểu float32."""
    import cv2

    gx, gy = reference_sobel_gradients(gray)
    return cv2.magnitude(gx, gy)


def run_reference_pipeline(
    rgb: NDArray[np.uint8], ksize: int = 3, threshold: float = 100.0
) -> PipelineResult:
    """Chạy nhánh tham chiếu với cùng quy tắc phân ngưỡng và tạo tranh.

    Ghi rõ sai khác mức xám nếu dùng cv2.cvtColor. Đối chiếu riêng các bộ lọc
    phải dùng cùng một ảnh xám để sai số mức xám không lan sang bước sau.
    """
    from processing.sketch import render_sketch, threshold_edges

    ksize, threshold = validate_params(ksize, threshold)
    validate_rgb(rgb)

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
