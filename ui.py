"""Khung giao diện Tkinter.

Long phụ trách bố cục, vùng xem ảnh và điều khiển tham số.
Kiệt nối chức năng mở/lưu và thông báo lỗi sau khi thống nhất hàm sự kiện.
Nhập module này không tạo cửa sổ và không đọc ảnh.
"""

from __future__ import annotations

from tkinter import Misc, filedialog, messagebox

import numpy as np
from numpy.typing import NDArray

from image_io import load_rgb, save_sketch


def open_image_dialog(parent: Misc) -> NDArray[np.uint8] | None:
    """Kiệt: chọn và đọc ảnh; trả None nếu hủy hoặc có lỗi, giữ ảnh cũ ở mã gọi."""
    filename = filedialog.askopenfilename(
        parent=parent,
        title="Mở ảnh JPG hoặc PNG",
        filetypes=[("Ảnh JPG và PNG", "*.jpg *.jpeg *.png"), ("Mọi tệp", "*.*")],
    )
    if not filename:
        return None
    try:
        return load_rgb(filename)
    except (OSError, ValueError) as exc:
        messagebox.showerror("Không mở được ảnh", str(exc), parent=parent)
        return None


def save_sketch_dialog(sketch: NDArray[np.uint8] | None, parent: Misc) -> bool:
    """Kiệt: chọn nơi lưu tranh; trả True chỉ khi ghi thành công."""
    if sketch is None:
        messagebox.showerror("Chưa có tranh", "Hãy xử lý ảnh trước khi lưu.", parent=parent)
        return False
    filename = filedialog.asksaveasfilename(
        parent=parent,
        title="Lưu tranh PNG",
        defaultextension=".png",
        filetypes=[("Ảnh PNG", "*.png")],
    )
    if not filename:
        return False
    try:
        save_sketch(filename, sketch)
    except (OSError, ValueError) as exc:
        messagebox.showerror("Không lưu được tranh", str(exc), parent=parent)
        return False
    return True


def launch_app() -> None:
    """Khởi tạo cửa sổ và chạy vòng lặp Tkinter sau khi triển khai.

    Giao diện dự kiến có nút Mở ảnh, Xử lý, Lưu tranh; lựa chọn k=3/5,
    ngưỡng T và các vùng xem ảnh gốc, trung gian, tranh cuối.
    """
    raise NotImplementedError("Long phụ trách triển khai bố cục giao diện Tkinter.")
