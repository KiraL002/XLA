"""Đọc JPG/PNG và lưu tranh nhị phân bằng Pillow. Phụ trách: Kiệt."""

from __future__ import annotations

from os import PathLike
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageOps


def _path(path: str | PathLike[str]) -> Path:
    """Chuyển đường dẫn; phân biệt dữ liệu sai với lỗi đọc/ghi của hệ điều hành."""
    if not isinstance(path, (str, PathLike)):
        raise ValueError("Đường dẫn phải là chuỗi hoặc đối tượng đường dẫn.")
    try:
        if not os.fspath(path) or "\x00" in os.fspath(path):
            raise ValueError("Đường dẫn không được rỗng hoặc chứa ký tự NUL.")
        return Path(path)
    except (TypeError, ValueError) as exc:
        raise ValueError("Đường dẫn ảnh không hợp lệ.") from exc


def load_rgb(path: str | PathLike[str]) -> NDArray[np.uint8]:
    """Đọc JPG/PNG, trả mảng RGB uint8 có dạng (H, W, 3).

    Ảnh xám được chuyển sang RGB trước khi trả về. Ảnh phải có H, W > 0.
    Không mở hộp thoại tại đây; đường dẫn do giao diện hoặc mã gọi cung cấp.
    Lỗi đọc tệp phải được báo cho mã gọi, không trả ảnh thay thế.
    """
    source = _path(path)
    with Image.open(source) as image:
        if image.format not in {"JPEG", "PNG"}:
            raise ValueError("Chỉ hỗ trợ nội dung ảnh JPEG hoặc PNG.")
        # Sửa hướng ảnh từ điện thoại theo EXIF trước khi chuyển sang mảng RGB.
        oriented = ImageOps.exif_transpose(image)
        if "A" in oriented.getbands() or "transparency" in oriented.info:
            rgba = oriented.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            rgb_image = Image.alpha_composite(background, rgba).convert("RGB")
        else:
            rgb_image = oriented.convert("RGB")
        # Sao chép dữ liệu để mảng dùng được sau khi tệp đã đóng.
        return np.array(rgb_image, dtype=np.uint8, copy=True)


def save_sketch(path: str | PathLike[str], sketch: NDArray[np.uint8]) -> None:
    """Lưu tranh (H, W), uint8, giá trị 0/255 ra PNG.

    Không thay đổi sketch. Báo lỗi cho mã gọi nếu dữ liệu sai hoặc lưu thất bại.
    Phần mở hộp thoại và thông báo nằm ở giao diện.
    """
    if not isinstance(sketch, np.ndarray) or sketch.dtype != np.uint8:
        raise ValueError("Tranh phải là mảng NumPy uint8.")
    if sketch.ndim != 2 or sketch.size == 0:
        raise ValueError("Tranh phải có dạng (H, W) với H, W dương.")
    if not ((sketch == 0) | (sketch == 255)).all():
        raise ValueError("Tranh chỉ được chứa giá trị 0 và 255.")
    destination = _path(path)
    if destination.suffix.lower() != ".png":
        raise ValueError("Đường dẫn lưu tranh phải có đuôi .png.")

    # Ghi tệp tạm cùng thư mục rồi thay thế, tránh hỏng ảnh cũ nếu ghi thất bại.
    temporary = None
    try:
        with NamedTemporaryFile(
            dir=destination.parent, prefix=".sketch-", suffix=".png", delete=False
        ) as handle:
            temporary = Path(handle.name)
        Image.fromarray(sketch).save(temporary, format="PNG")
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
