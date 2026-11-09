"""Giao tiếp bộ điều phối các bước xử lý. Phụ trách: Long."""

from __future__ import annotations

import math
from typing import TypedDict

import numpy as np
from numpy.typing import NDArray

from processing.edges import sobel_magnitude
from processing.filters import mean_filter
from processing.grayscale import to_grayscale
from processing.sketch import render_sketch, threshold_edges

ALLOWED_KSIZES = (3, 5)
RESULT_KEYS = ("gray", "smooth", "magnitude", "edges", "sketch")


class PipelineResult(TypedDict):
    """Các khóa trả về cố định để giao diện và mã đánh giá dùng chung."""

    gray: NDArray[np.float32]
    smooth: NDArray[np.float32]
    magnitude: NDArray[np.float32]
    edges: NDArray[np.bool_]
    sketch: NDArray[np.uint8]


def validate_params(ksize: int, threshold: float) -> tuple[int, float]:
    """Kiểm tra tham số; ném ValueError nếu sai. Trả về (ksize, threshold) chuẩn."""
    if isinstance(ksize, bool) or not isinstance(ksize, (int, np.integer)):
        raise ValueError("Kích thước cửa sổ phải là số nguyên 3 hoặc 5.")
    if int(ksize) not in ALLOWED_KSIZES:
        raise ValueError(f"Kích thước cửa sổ chỉ nhận 3 hoặc 5, nhận được {ksize}.")
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float, np.number)):
        raise ValueError("Ngưỡng phải là một số.")
    t = float(threshold)
    if not math.isfinite(t) or t < 0:
        raise ValueError(f"Ngưỡng phải là số hữu hạn không âm, nhận được {threshold}.")
    return int(ksize), t


def validate_rgb(rgb: NDArray[np.uint8]) -> None:
    """Kiểm tra ảnh RGB (H, W, 3) uint8; ném ValueError nếu sai."""
    if not isinstance(rgb, np.ndarray):
        raise ValueError("Ảnh đầu vào phải là mảng NumPy.")
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError(f"Ảnh đầu vào phải có dạng H×W×3 (RGB), nhận được {rgb.shape}.")
    if rgb.shape[0] < 1 or rgb.shape[1] < 1:
        raise ValueError("Ảnh đầu vào không được rỗng.")
    if rgb.dtype != np.uint8:
        raise ValueError(f"Ảnh RGB phải là uint8, nhận được {rgb.dtype}.")


def run_pipeline(
    rgb: NDArray[np.uint8], ksize: int = 3, threshold: float = 100.0
) -> PipelineResult:
    """Nối mức xám → làm mịn → Sobel → phân ngưỡng → tạo tranh.

    Đầu vào RGB (H, W, 3), uint8; tham số theo docs/INTERFACES.md.
    Trả đúng 5 khóa đã khai báo, mỗi mảng có dạng (H, W).
    Không đọc/lưu tệp, không mở giao diện và không sửa rgb.
    Bước phân ngưỡng nhận độ lớn gradient thô, không phải ảnh xem trước.
    """
    ksize, threshold = validate_params(ksize, threshold)
    validate_rgb(rgb)

    gray = to_grayscale(rgb)
    smooth = mean_filter(gray, ksize)
    magnitude = sobel_magnitude(smooth)
    edges = threshold_edges(magnitude, threshold)
    sketch = render_sketch(edges)

    return {
        "gray": gray,
        "smooth": smooth,
        "magnitude": magnitude,
        "edges": edges,
        "sketch": sketch,
    }


def magnitude_preview(magnitude: NDArray[np.float32]) -> NDArray[np.uint8]:
    """Ảnh uint8 chỉ để XEM: chia cho giá trị lớn nhất rồi nhân 255.

    Không dùng kết quả này làm đầu vào xử lý, lưu hay đo.
    """
    m = np.asarray(magnitude, dtype=np.float32)
    peak = float(m.max()) if m.size else 0.0
    if peak <= 0.0:
        return np.zeros(m.shape, dtype=np.uint8)
    return np.clip(m * (255.0 / peak), 0, 255).astype(np.uint8)