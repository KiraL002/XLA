"""Giao tiếp bộ điều phối các bước xử lý. Phụ trách: Long."""

from __future__ import annotations

from typing import TypedDict

import numpy as np
from numpy.typing import NDArray


class PipelineResult(TypedDict):
    """Các khóa trả về cố định để giao diện và mã đánh giá dùng chung."""

    gray: NDArray[np.float32]
    smooth: NDArray[np.float32]
    magnitude: NDArray[np.float32]
    edges: NDArray[np.bool_]
    sketch: NDArray[np.uint8]


def run_pipeline(
    rgb: NDArray[np.uint8], ksize: int = 3, threshold: float = 100.0
) -> PipelineResult:
    """Nối mức xám → làm mịn → Sobel → phân ngưỡng → tạo tranh.

    Đầu vào RGB (H, W, 3), uint8; tham số theo docs/INTERFACES.md.
    Trả đúng 5 khóa đã khai báo, mỗi mảng có dạng (H, W).
    Không đọc/lưu tệp, không mở giao diện và không sửa rgb.
    Hiện chưa nối các hàm, không tạo ảnh kết quả thay thế.
    """
    raise NotImplementedError("Long phụ trách triển khai run_pipeline khi ghép các module.")
