"""Khai báo đọc/lưu ảnh bằng Pillow. Phụ trách: Kiệt."""

from __future__ import annotations

from os import PathLike

import numpy as np
from numpy.typing import NDArray


def load_rgb(path: str | PathLike[str]) -> NDArray[np.uint8]:
    """Đọc JPG/PNG, trả mảng RGB uint8 có dạng (H, W, 3).

    Ảnh xám được chuyển sang RGB trước khi trả về. Ảnh phải có H, W > 0.
    Không mở hộp thoại tại đây; đường dẫn do giao diện hoặc mã gọi cung cấp.
    Lỗi đọc tệp phải được báo cho mã gọi, không trả ảnh thay thế.
    """
    raise NotImplementedError("Kiệt phụ trách triển khai load_rgb.")


def save_sketch(path: str | PathLike[str], sketch: NDArray[np.uint8]) -> None:
    """Lưu tranh (H, W), uint8, giá trị 0/255 ra PNG.

    Không thay đổi sketch. Báo lỗi cho mã gọi nếu dữ liệu sai hoặc lưu thất bại.
    Phần mở hộp thoại và thông báo nằm ở giao diện.
    """
    raise NotImplementedError("Kiệt phụ trách triển khai save_sketch.")
