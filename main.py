"""Điểm chạy giao diện và kiểm tra môi trường của ứng dụng."""

from __future__ import annotations

import argparse
import importlib
import sys

PROJECT_TITLE = (
    "Hệ thống chuyển ảnh thành tranh vẽ bằng các kỹ thuật xử lý ảnh truyền thống"
)

# Danh sách giao tiếp đã thống nhất; nhập module không được tự mở giao diện.
MODULE_INTERFACES = {
    "image_io": ("load_rgb", "save_sketch"),
    "processing.grayscale": ("to_grayscale",),
    "processing.filters": ("mean_filter",),
    "processing.edges": ("sobel_magnitude", "sobel_gradients"),
    "processing.sketch": ("threshold_edges", "render_sketch"),
    "pipeline": ("run_pipeline",),
    "ui": ("launch_app", "open_image_dialog", "save_sketch_dialog"),
    "evaluation.reference": (
        "reference_grayscale",
        "reference_mean_filter",
        "reference_sobel_magnitude",
        "run_reference_pipeline",
    ),
    "evaluation.benchmark": ("measure_runtime",),
}


def check_imports() -> int:
    """Kiểm tra việc nhập module và tên hàm."""
    failed = False
    for module_name, function_names in MODULE_INTERFACES.items():
        try:
            module = importlib.import_module(module_name)
            missing = [
                name for name in function_names
                if not callable(getattr(module, name, None))
            ]
            if missing:
                raise AttributeError("Thiếu hàm: " + ", ".join(missing))
        except Exception as exc:
            failed = True
            print(f"[LỖI] {module_name}: {exc}", file=sys.stderr)
        else:
            print(f"[OK] {module_name}")
    if not failed:
        print("Nhập module thành công (chỉ xác nhận nhập module và tên hàm, chưa chạy thuật toán).")
    return int(failed)


def check_dependencies() -> int:
    """Kiểm tra thư viện hiện có trong đúng môi trường Python đang chạy."""
    failed = False
    for module_name in ("numpy", "PIL", "cv2", "tkinter"):
        try:
            importlib.import_module(module_name)
        except ImportError as exc:
            failed = True
            print(f"[THIẾU] {module_name}: {exc}", file=sys.stderr)
        else:
            print(f"[OK] {module_name}")
    if failed:
        print("Xem README.md để cài thư viện trong môi trường ảo.")
    return int(failed)


def main() -> int:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--check", action="store_true", help="Kiểm tra nhập module và tên hàm")
    actions.add_argument("--check-deps", action="store_true", help="Kiểm tra thư viện đã cài")
    actions.add_argument("--gui", action="store_true", help="Mở giao diện")
    args = parser.parse_args()

    if args.check:
        return check_imports()
    if args.check_deps:
        return check_dependencies()
    if args.gui:
        try:
            from ui import launch_app
            launch_app()
        except NotImplementedError as exc:
            print(f"Chưa thể chạy giao diện: {exc}", file=sys.stderr)
            return 2
        except ImportError as exc:
            print(f"Thiếu module hoặc thư viện: {exc}", file=sys.stderr)
            return 1
        return 0

    print(PROJECT_TITLE)
    print("Luồng: RGB → mức xám → lọc trung bình → Sobel → phân ngưỡng → tranh nét.")
    print("Mở giao diện: python main.py --gui")
    print("Kiểm tra cấu trúc: python main.py --check")
    print("Kiểm tra thư viện: python main.py --check-deps")
    print("Bắt đầu đọc README.md và docs/INTERFACES.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
