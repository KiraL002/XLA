# Hướng dẫn phần việc của Kiệt

Bộ ảnh và các phần chuẩn bị bổ sung ngày 06/11/2026 được tổng hợp tại
`KIET_CHUAN_BI_TRONG_KHI_CHO.md`.

## Các phần đã cài đặt

| Tệp | Chức năng |
| --- | --- |
| `image_io.py` | Đọc JPEG/PNG thành RGB; lưu tranh nhị phân thành PNG |
| `processing/grayscale.py` | Chuyển RGB thành mức xám bằng công thức tự viết |
| `processing/sketch.py` | Chọn biên theo ngưỡng và tạo nét đen nền trắng |
| `evaluation/reference.py` | Hàm `reference_grayscale` đối chiếu OpenCV |
| `ui.py` | Hàm mở/lưu bằng hộp thoại, xử lý hủy thao tác và báo lỗi |
| `tests/test_*.py` | Kiểm thử mức xám, tạo tranh, đọc/lưu và hộp thoại |
| `demo_kiet.py` | Chạy riêng các bước của Kiệt trước khi ghép hệ thống |

Bộ lọc, Sobel, bộ điều phối, công cụ đo và bố cục giao diện vẫn do Hiếu/Long
triển khai. Hai hàm sự kiện đã sẵn sàng để gọi, chưa được nối với nút bấm
trong ứng dụng hoàn chỉnh vì chưa có bố cục giao diện của Long.

## Hiểu các phép xử lý

**Mức xám.** Tại mỗi điểm, tính `Y = 0.299R + 0.587G + 0.114B`.
Ví dụ đỏ `[255,0,0]` cho 76.245; xanh lục cho 149.685; xanh lam cho 29.07.
Giữ float32 để không mất phần thập phân trước khi truyền sang bộ lọc.
Đây là tổng có trọng số, không phải trung bình cộng ba kênh.

**Phân ngưỡng.** Nhận độ lớn gradient thô do Sobel cung cấp; điểm có `M > T`
là biên, điểm bằng T không là biên. M có thể lớn hơn 255. Không chuẩn hóa M
trước khi so sánh. T càng lớn thường càng ít nét; tác dụng thẩm mỹ cần đánh
giá trên ảnh thật sau khi ghép Sobel.

**Tạo tranh.** Tạo mảng mới, đổi True thành nét đen 0, False thành nền trắng 255.
Kết quả là tranh đường nét đen trắng, chưa có sắc độ chì. Không sửa mảng đầu vào.

## Đọc và lưu ảnh

- Kiểm tra định dạng theo nội dung tệp: chỉ JPEG/PNG. Ảnh xám được mở thành RGB.
- Sửa hướng theo EXIF. PNG có alpha được ghép trên nền trắng khi nạp ảnh.
- JPEG có nén mất dữ liệu nên không kiểm tra bằng cách đòi giá trị giống tuyệt
  đối ảnh trước nén. PNG đầu ra phải bảo toàn chính xác các giá trị 0/255.
- Lưu chỉ nhận mảng uint8 2 chiều không rỗng, giá trị 0/255 và đường dẫn `.png`.
  Thư mục đích phải tồn tại. Ghi tệp tạm cùng thư mục rồi thay tệp đích để
  tránh làm hỏng tệp cũ nếu thao tác ghi thất bại.
- Dữ liệu sai báo ValueError; lỗi tệp báo OSError hoặc lớp con. Phần UI hiện
  thông báo thay vì trả kết quả giả.

## Chạy và kiểm tra

Trong PowerShell, sau khi cài requirements vào môi trường ảo:

```powershell
cd D:\XLA\tranh_ve
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py --check
.\.venv\Scripts\python.exe main.py --check-deps
```

Demo mức xám và đối chiếu OpenCV trên ảnh của nhóm:

```powershell
.\.venv\Scripts\python.exe demo_kiet.py --image "D:\duong_dan\anh_cua_nhom.jpg"
```

Demo phân ngưỡng trên ma trận kiểm thử, không cần đợi Sobel:

```powershell
.\.venv\Scripts\python.exe demo_kiet.py --magnitude data/test_matrices/threshold_3x5.csv --threshold 100
```

Đầu ra trong `results/kiet/`: bản xem trước mức xám, dữ liệu float32 nếu cấp
ảnh; tranh từ ma trận nếu cấp gradient; và `demo_report.json` với sai số tính
thực lúc chạy. Ma trận 3×5 là dữ liệu kiểm thử số học, không phải kết quả phát
hiện biên từ ảnh thật; với T=100 phải có 5 điểm biên.

## Nối với giao diện của Long

Hai hàm trong `ui.py` nhận cửa sổ cha để hộp thoại thuộc đúng ứng dụng:

```python
from ui import open_image_dialog, save_sketch_dialog

# Trong sự kiện Mở ảnh của giao diện do Long viết:
candidate = open_image_dialog(root)
if candidate is not None:
    current_rgb = candidate
    current_sketch = None  # Ảnh mới làm kết quả cũ không còn hợp lệ.
    # Long cập nhật vùng xem ảnh và trạng thái nút Lưu.

# Trong sự kiện Lưu, dùng tranh gốc, không dùng bản xem trước thu nhỏ:
saved = save_sketch_dialog(current_sketch, root)
```

`open_image_dialog` trả None khi hủy/lỗi; mã gọi giữ nguyên ảnh cũ khi nhận None.
`save_sketch_dialog` trả True chỉ khi ghi thành công; False khi hủy/lỗi hoặc
chưa có tranh. Các kiểm thử hộp thoại dùng giả lập, không tạo cửa sổ thật.
Sau khi ghép bố cục, kiểm tra hiển thị và thao tác thủ công: mở, hủy mở,
đổi ảnh, lưu tranh, hủy lưu và lỗi quyền ghi.

## Nguồn kỹ thuật

- [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html): đọc/chuyển định dạng/lưu ảnh.
- [OpenCV RGB và mức xám](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html): công thức và COLOR_RGB2GRAY.
- [Tkinter dialogs](https://docs.python.org/3/library/dialog.html): hộp thoại chọn tệp.
