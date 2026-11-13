"""Phân ngưỡng và tạo tranh bằng NumPy."""

from __future__ import annotations

import math
from numbers import Real

import numpy as np
from numpy.typing import NDArray

from processing.filters import mean_filter


def threshold_edges(
    magnitude: NDArray[np.float32], threshold: float = 100.0
) -> NDArray[np.bool_]:
    """Trả mặt nạ (H, W), bool theo quy tắc magnitude > threshold.

    magnitude là độ lớn gradient thô float32, hữu hạn, không âm.
    threshold là số hữu hạn không âm. Giá trị đúng bằng ngưỡng không là biên.
    Không sửa đầu vào; dữ liệu sai phải báo ValueError khi triển khai.
    """
    if not isinstance(magnitude, np.ndarray) or magnitude.dtype != np.float32:
        raise ValueError("Độ lớn gradient phải là mảng NumPy float32.")
    if magnitude.ndim != 2 or magnitude.size == 0:
        raise ValueError("Độ lớn gradient phải có dạng (H, W) với H, W dương.")
    if not np.isfinite(magnitude).all() or (magnitude < 0).any():
        raise ValueError("Độ lớn gradient phải hữu hạn và không âm.")
    if isinstance(threshold, (bool, np.bool_)) or not isinstance(threshold, Real):
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.")
    try:
        value = float(threshold)
    except (ValueError, OverflowError) as exc:
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.") from exc
    if not math.isfinite(value) or value < 0:
        raise ValueError("Ngưỡng phải là một số thực hữu hạn không âm.")

    # So sánh gradient thô; giữ độ chính xác của ngưỡng do người dùng nhập.
    return magnitude > np.float64(value)


def _validate_edge_mask(edges: NDArray[np.bool_]) -> None:
    if not isinstance(edges, np.ndarray) or edges.dtype != np.bool_:
        raise ValueError("Mặt nạ biên phải là mảng NumPy bool.")
    if edges.ndim != 2 or edges.size == 0:
        raise ValueError("Mặt nạ biên phải có dạng (H, W) với H, W dương.")


def thin_edges(edges: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """Làm mảnh mặt nạ bằng Zhang–Suen với hai lượt xóa trong mỗi vòng lặp."""
    _validate_edge_mask(edges)
    # Xem phần ngoài ảnh là nền để xử lý được cả nét sát rìa.
    padded = np.pad(edges, 1, mode="constant")
    center = padded[1:-1, 1:-1]
    north = padded[:-2, 1:-1]
    east = padded[1:-1, 2:]
    south = padded[2:, 1:-1]
    west = padded[1:-1, :-2]
    neighbors = (north, padded[:-2, 2:], east, padded[2:, 2:],
                 south, padded[2:, :-2], west, padded[:-2, :-2])

    while True:
        changed = False
        for first_pass in (True, False):
            count = np.zeros(edges.shape, dtype=np.uint8)
            transitions = np.zeros_like(count)
            for previous, current in zip(neighbors[-1:] + neighbors[:-1], neighbors):
                count += current
                transitions += ~previous & current

            if first_pass:
                blocked = (north & east & south) | (east & south & west)
            else:
                blocked = (north & east & west) | (north & south & west)
            removable = center & (count >= 2) & (count <= 6) & (transitions == 1) & ~blocked
            if removable.any():
                center[removable] = False
                changed = True
        if not changed:
            return center


def render_sketch(edges: NDArray[np.bool_]) -> NDArray[np.uint8]:
    """Đổi mặt nạ bool thành tranh uint8 với nét đen 0 và nền trắng 255."""
    _validate_edge_mask(edges)

    # True là nét đen; các điểm còn lại giữ nền trắng.
    sketch = np.full(edges.shape, 255, dtype=np.uint8)
    sketch[edges] = 0
    return sketch


def render_pencil(
    smooth: NDArray[np.float32], magnitude: NDArray[np.float32], edges: NDArray[np.bool_]
) -> NDArray[np.uint8]:
    """Dựng bóng bằng nét gạch và thêm lớp nét nhấn từ mặt nạ Sobel."""
    local_mean = mean_filter(smooth, 5)
    low, high = np.percentile(smooth, (2, 98))
    span = float(high - low)
    # Giới hạn mức giãn tương phản để ảnh gần phẳng không bị khuếch đại quá mạnh.
    if span >= 24:
        brightness = np.clip((smooth - np.float32(low)) / span, 0, 1)
    else:
        brightness = smooth / 255.0
    shade = (1.0 - brightness) ** 1.55

    # Hai hướng gạch có bước khác nhau. Hướng thứ hai đậm lên chủ yếu trong bóng sâu.
    height, width = smooth.shape
    rows = np.arange(height)
    columns = np.arange(width)
    hatch_pattern = np.clip(1.0 - np.abs(np.arange(9) - 4) / 2.25, 0, 1).astype(np.float32)
    cross_pattern = np.clip(1.0 - np.abs(np.arange(13) - 6) / 2.5, 0, 1).astype(np.float32)
    hatch_phase = ((rows % 9).astype(np.uint8)[:, None] + ((columns + 3) % 9).astype(np.uint8)) % 9
    cross_phase = ((-rows % 13).astype(np.uint8)[:, None] + ((2 * columns + 5) % 13).astype(np.uint8)) % 13
    paper = 1.0 - shade * (0.14 + 0.58 * hatch_pattern[hatch_phase])
    paper *= 1.0 - 0.32 * shade**2 * cross_pattern[cross_phase]

    # Giữ một lớp viền nhẹ. Ngưỡng và làm mảnh chỉ tác động lên nét nhấn.
    detail = np.clip((local_mean - smooth) / max(10.0, 0.09 * span), 0, 1)
    contour = np.clip(magnitude / max(35.0, 1.2 * span), 0, 1)
    pencil = 255.0 * paper * (1.0 - 0.64 * detail) * (1.0 - 0.24 * contour)
    pencil *= 1.0 - 0.36 * contour * edges
    return np.rint(pencil).astype(np.uint8)
