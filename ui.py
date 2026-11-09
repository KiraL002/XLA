"""Giao diện Tkinter: bố cục, vùng xem ảnh, điều khiển tham số và nút bấm.

Phụ trách bố cục: Long. Hàm sự kiện mở/lưu (on_open_clicked, on_save_clicked)
là chỗ Kiệt nối image_io; bản dưới đây là bản chạy được để cả nhóm thử sớm.

Xử lý chỉ chạy khi bấm nút "Xử lý" để tránh chạy lại liên tục trên ảnh lớn.
Ảnh hiển thị được thu nhỏ CHỈ để xem; dữ liệu đem lưu/đo luôn là mảng gốc.
"""

from __future__ import annotations

import numpy as np

import image_io
from pipeline import ALLOWED_KSIZES, PipelineResult, magnitude_preview, run_pipeline

DEFAULT_KSIZE = 3
DEFAULT_THRESHOLD = 100.0

try:  # nhập module không được lỗi khi thiếu Tkinter; launch_app sẽ báo ImportError
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    from PIL import Image, ImageTk
except ImportError as _exc:  # pragma: no cover
    tk = None
    _TK_IMPORT_ERROR = _exc

# (nhãn hiển thị, khóa nội bộ)
VIEWS = (
    ("Ảnh gốc", "rgb"),
    ("Mức xám", "gray"),
    ("Làm mịn", "smooth"),
    ("Độ lớn gradient (xem trước)", "magnitude"),
    ("Mặt nạ biên", "edges"),
    ("Tranh nét", "sketch"),
)
THRESHOLD_MAX = 500.0  # chỉ là giới hạn thanh trượt; M thô có thể lớn hơn


def to_display_array(key: str, rgb, result: PipelineResult | None):
    """Đổi dữ liệu thành mảng uint8 (xám hoặc RGB) để HIỂN THỊ. Trả None nếu chưa có."""
    if key == "rgb":
        return rgb
    if result is None:
        return None
    if key in ("gray", "smooth"):
        return np.clip(result[key], 0, 255).astype(np.uint8)
    if key == "magnitude":
        return magnitude_preview(result["magnitude"])
    if key == "edges":
        return np.where(result["edges"], 255, 0).astype(np.uint8)
    if key == "sketch":
        return result["sketch"]
    return None


class App:
    def __init__(self, root) -> None:
        self.root = root
        root.title("Chuyển ảnh thành tranh nét - Xử lý ảnh")
        root.geometry("1000x700")
        root.minsize(720, 520)

        self.rgb: np.ndarray | None = None
        self.result: PipelineResult | None = None
        self._photo: ImageTk.PhotoImage | None = None  # giữ tham chiếu, tránh bị thu gom

        self.ksize_var = tk.IntVar(value=DEFAULT_KSIZE)
        self.threshold_var = tk.DoubleVar(value=DEFAULT_THRESHOLD)
        self.view_var = tk.StringVar(value=VIEWS[0][0])
        self.status_var = tk.StringVar(value="Hãy mở một ảnh JPG hoặc PNG.")

        self._build_layout()

    # ------------------------------------------------------------------ bố cục
    def _build_layout(self) -> None:
        bar = ttk.Frame(self.root, padding=6)
        bar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open = ttk.Button(bar, text="Mở ảnh", command=self.on_open_clicked)
        self.btn_open.pack(side=tk.LEFT, padx=2)
        self.btn_process = ttk.Button(
            bar, text="Xử lý", command=self.on_process_clicked, state=tk.DISABLED
        )
        self.btn_process.pack(side=tk.LEFT, padx=2)
        self.btn_save = ttk.Button(
            bar, text="Lưu tranh (PNG)", command=self.on_save_clicked, state=tk.DISABLED
        )
        self.btn_save.pack(side=tk.LEFT, padx=2)

        ttk.Separator(bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Label(bar, text="Cửa sổ làm mịn:").pack(side=tk.LEFT)
        for k in ALLOWED_KSIZES:
            ttk.Radiobutton(
                bar, text=f"{k}×{k}", value=k, variable=self.ksize_var
            ).pack(side=tk.LEFT, padx=2)

        ttk.Label(bar, text="  Ngưỡng:").pack(side=tk.LEFT)
        self.threshold_scale = ttk.Scale(
            bar, from_=0.0, to=THRESHOLD_MAX, variable=self.threshold_var,
            orient=tk.HORIZONTAL, length=180,
        )
        self.threshold_scale.pack(side=tk.LEFT, padx=4)
        self.threshold_entry = ttk.Spinbox(
            bar, from_=0.0, to=THRESHOLD_MAX, increment=1.0, width=7,
            textvariable=self.threshold_var,
        )
        self.threshold_entry.pack(side=tk.LEFT)

        style = ttk.Style(self.root)
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "white")],
            selectbackground=[("readonly", "white")],
            selectforeground=[("readonly", "black")],
        )

        view_bar = ttk.Frame(self.root, padding=(6, 0))
        view_bar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(view_bar, text="Xem:").pack(side=tk.LEFT)
        self.view_combo = ttk.Combobox(
            view_bar, state="readonly", width=32,
            values=[label for label, _ in VIEWS], textvariable=self.view_var,
        )
        self.view_combo.pack(side=tk.LEFT, padx=4)
        self.view_combo.bind("<<ComboboxSelected>>", self._on_view_selected)

        self.canvas = tk.Canvas(self.root, background="#e8e8e8", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.canvas.bind("<Configure>", lambda _e: self.refresh_view())

        ttk.Label(self.root, textvariable=self.status_var, anchor=tk.W, padding=(8, 2)).pack(
            side=tk.BOTTOM, fill=tk.X
        )

    # ---------------------------------------------------------------- hiển thị
    def _current_key(self) -> str:
        label = self.view_var.get()
        return next(key for lab, key in VIEWS if lab == label)
    
    def _on_view_selected(self, _event=None) -> None:
        self.view_combo.selection_clear()
        self.canvas.focus_set()  
        self.refresh_view()

    def refresh_view(self) -> None:
        self.canvas.delete("all")
        arr = to_display_array(self._current_key(), self.rgb, self.result)
        if arr is None:
            msg = "Chưa có ảnh." if self.rgb is None else "Bấm \"Xử lý\" để xem bước này."
            self.canvas.create_text(
                self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                text=msg, fill="#666666",
            )
            self._photo = None
            return
        img = Image.fromarray(arr)
        cw, ch = max(self.canvas.winfo_width(), 1), max(self.canvas.winfo_height(), 1)
        scale = min(cw / img.width, ch / img.height, 1.0)  # chỉ thu nhỏ để xem
        if scale < 1.0:
            img = img.resize(
                (max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                Image.LANCZOS,
            )
        self._photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(cw // 2, ch // 2, image=self._photo, anchor=tk.CENTER)

    # ------------------------------------------------------------ đọc tham số
    def _read_params(self) -> tuple[int, float]:
        try:
            ksize = int(self.ksize_var.get())
            threshold = float(self.threshold_var.get())
        except (tk.TclError, ValueError):
            raise ValueError("Ngưỡng phải là một số hợp lệ.") from None
        return ksize, threshold

    # ------------------------------------------------------------ hàm sự kiện
    def on_open_clicked(self) -> None:
        """Mở ảnh. Kiệt có thể tinh chỉnh thông báo lỗi/định dạng tệp tại đây."""
        path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Ảnh JPG/PNG", "*.jpg *.jpeg *.png"), ("Tất cả", "*.*")],
        )
        if not path:  # người dùng hủy chọn tệp: không đổi trạng thái, không báo lỗi
            return
        try:
            rgb = image_io.load_rgb(path)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Không đọc được ảnh", str(exc))
            return
        except NotImplementedError:
            messagebox.showerror("Chưa triển khai", "Hàm load_rgb chưa được triển khai.")
            return
        self.rgb = rgb
        self.result = None
        self.btn_process.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.DISABLED)
        self.view_var.set(VIEWS[0][0])
        self.status_var.set(f"Đã mở: {path}  ({rgb.shape[1]}×{rgb.shape[0]})")
        self.refresh_view()

    def on_process_clicked(self) -> None:
        if self.rgb is None:
            messagebox.showwarning("Chưa có ảnh", "Hãy mở ảnh trước khi xử lý.")
            return
        try:
            ksize, threshold = self._read_params()
            self.root.config(cursor="watch")
            self.root.update_idletasks()
            result = run_pipeline(self.rgb, ksize, threshold)
        except ValueError as exc:
            messagebox.showerror("Tham số không hợp lệ", str(exc))
            return
        except NotImplementedError as exc:
            messagebox.showerror("Chưa triển khai", f"Một bước xử lý chưa hoàn thành: {exc}")
            return
        finally:
            self.root.config(cursor="")
        self.result = result
        self.btn_save.config(state=tk.NORMAL)
        self.view_var.set(VIEWS[-1][0])
        n_edge = int(result["edges"].sum())
        self.status_var.set(
            f"Xong: cửa sổ {ksize}×{ksize}, ngưỡng {threshold:g}, "
            f"{n_edge} điểm biên ({n_edge / result['edges'].size:.1%})."
        )
        self.refresh_view()

    def on_save_clicked(self) -> None:
        """Lưu tranh cuối ra PNG (mảng gốc, không phải ảnh đã thu nhỏ)."""
        if self.result is None:
            messagebox.showwarning("Chưa có tranh", "Hãy bấm Xử lý trước khi lưu.")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu tranh", defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if not path:
            return
        try:
            image_io.save_sketch(path, self.result["sketch"])
        except (OSError, ValueError) as exc:
            messagebox.showerror("Lưu thất bại", str(exc))
            return
        except NotImplementedError:
            messagebox.showerror("Chưa triển khai", "Hàm save_sketch chưa được triển khai.")
            return
        self.status_var.set(f"Đã lưu: {path}")


def launch_app() -> None:
    """Khởi tạo cửa sổ và chạy vòng lặp Tkinter (theo docs/INTERFACES.md)."""
    if tk is None:
        raise ImportError(f"Không có Tkinter/Pillow để mở giao diện: {_TK_IMPORT_ERROR}")
    root = tk.Tk()
    App(root)
    root.mainloop()