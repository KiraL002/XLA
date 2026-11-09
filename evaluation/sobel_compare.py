"""So sánh Sobel tự viết với nhánh OpenCV (Long): MAE, sai số lớn nhất, tỷ lệ điểm khác.

Dùng cùng ảnh xám float32, ksize=3, BORDER_REPLICATE (xem evaluation/reference.py).
Chỉ ghi số vào báo cáo sau khi chạy thật trên bộ ảnh chung.
"""

from __future__ import annotations

import numpy as np

from evaluation.reference import reference_sobel_gradients, reference_sobel_magnitude
from processing.edges import sobel_gradients, sobel_magnitude


def _errors(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    d = np.abs(a.astype(np.float64) - b.astype(np.float64))  # đo trên số thực, chưa ép kiểu
    return float(d.mean()), float(d.max())


def compare_sobel(gray: np.ndarray) -> dict:
    """Trả MAE và sai số lớn nhất của Gx, Gy, M giữa bản tự viết và OpenCV.

    Chỉ ghi các giá trị này vào báo cáo sau khi chạy thật trên bộ ảnh chung.
    """
    gx, gy = sobel_gradients(gray)
    rgx, rgy = reference_sobel_gradients(gray)
    m, rm = sobel_magnitude(gray), reference_sobel_magnitude(gray)
    out = {}
    for name, a, b in (("gx", gx, rgx), ("gy", gy, rgy), ("magnitude", m, rm)):
        out[f"{name}_mae"], out[f"{name}_max"] = _errors(a, b)
    return out


def edge_mask_difference_ratio(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    """Tỷ lệ điểm khác nhau giữa hai mặt nạ/tranh cùng kích thước."""
    if mask_a.shape != mask_b.shape:
        raise ValueError("Hai mặt nạ phải cùng kích thước.")
    return float(np.count_nonzero(mask_a != mask_b)) / mask_a.size