# Kiểm thử

Chạy từ thư mục dự án:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

| Tệp | Phạm vi |
| --- | --- |
| `test_filters.py` | Lọc trung bình, xử lý rìa, kích thước cửa sổ và dữ liệu đầu vào |
| `test_edges.py` | Sobel, cạnh ngang/dọc, ảnh nhỏ và đối chiếu OpenCV |
| `test_grayscale.py` | Chuyển mức xám, kiểu dữ liệu và sai số so với OpenCV |
| `test_sketch.py` | Quy tắc ngưỡng, làm mảnh và tạo tranh nhị phân |
| `test_image_io.py` | Đọc JPG/PNG, lưu và mở lại PNG, xử lý lỗi đọc/ghi |
| `test_ui_io.py` | Hộp thoại mở/lưu với thao tác chọn, hủy và lỗi giả lập |
| `test_pipeline.py` | Tích hợp các bước, dữ liệu trung gian, tranh nét và tranh chì |

Các ma trận dùng kiểm tra số học nằm trong [bộ dữ liệu ma trận](../data/test_matrices/README.md).
Đối chiếu trên ảnh thật chạy bằng `python -m tools.evaluate_sketch`.
