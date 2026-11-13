# Kết quả kiểm thử phần Kiệt

Ngày kiểm tra: 04 tháng 11 năm 2026. Phạm vi: module của Kiệt, chưa phải
thực nghiệm đánh giá chất lượng tranh của toàn hệ thống.

## Môi trường thực chạy

Windows, Python 3.12.14 trong `.venv`; NumPy 2.5.4, Pillow 13.0.0,
opencv-python 5.0.0.93 (cv2 báo 5.0.0). Các phiên bản cài đặt được ghi trong
`requirements-kiet-tested.txt`. Dùng unittest, ảnh được tạo trong thư mục tạm.

## Kiểm thử tự động

| Tệp | Số ca | Kết quả |
| --- | --- | --- |
| `tests/test_grayscale.py` | 4 | Đạt |
| `tests/test_sketch.py` | 8 | Đạt |
| `tests/test_image_io.py` | 13 | Đạt |
| `tests/test_ui_io.py` | 7 | Đạt |
| Tổng | 32 | 0 thất bại, 0 lỗi, 0 bỏ qua |

Một số ca chứa nhiều đầu vào con qua subTest. Các nhóm đã kiểm tra:

- Giá trị RGB tính tay và mảng giả ngẫu nhiên 64×97, seed 2026, so OpenCV
  float32 với sai số tuyệt đối chấp nhận 5e-5. Đây là tiêu chí số học.
- M dưới/bằng/trên T, M lớn hơn 255, T=0, ngưỡng lớn và gần giá trị float32;
  từ chối ngưỡng âm, NaN, vô cực, bool hoặc không phải số.
- Kiểu, kích thước, mảng rỗng, dữ liệu sai, không sửa đầu vào, nền 255/nét 0.
- PNG/JPEG/ảnh xám, đường dẫn tiếng Việt, EXIF, PNG alpha/palette trong suốt.
- Tệp thiếu/hỏng/không hỗ trợ; PNG lưu đọc lại đúng; lỗi ghi giữ tệp cũ.
- Hộp thoại giả lập: chọn, hủy, chưa có tranh, lỗi mở/lưu; không tạo cửa sổ.

Chạy lại sau khi cài thư viện:

```powershell
cd D:\XLA\tranh_ve
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Môi trường tự động hạn chế thư mục tạm nên lần chạy đã đặt `tempfile.tempdir`
về `D:\XLA\tmp\kiet_tests` trước khi nạp unittest; logic kiểm thử không đổi.
Tóm tắt JSON được lưu tại `results/kiet/test_summary.json` ở lần chạy này.

## Demo đã chạy

```powershell
.\.venv\Scripts\python.exe demo_kiet.py --image results/kiet/rgb_test_input.png --magnitude data/test_matrices/threshold_3x5.csv --threshold 100
```

Ảnh RGB 20×120 là các ô màu do lặp dữ liệu tạo ra: đen, trắng, đỏ, xanh lục,
xanh lam và [10,20,30]. Đây là ảnh kiểm thử số học, không phải ảnh tự nhiên.

| Phép kiểm tra | Kết quả thực chạy |
| --- | --- |
| MAE mức xám so OpenCV trên ảnh ô màu | 0.0 |
| Sai số lớn nhất trên cùng ảnh ô màu | 0.0 |
| Ma trận gradient số học | 3×5, T=100 |
| Số điểm biên | 5 |
| Tranh lưu được | PNG một kênh, 3×5, giá trị 0/255 |
| `main.py --check` | Nhập module thành công |
| `main.py --check-deps` | Nhập được NumPy, Pillow, OpenCV và Tkinter |

Sai số bằng 0 chỉ áp dụng ảnh ô màu trên, không khẳng định mọi ảnh khớp tuyệt
đối. Chi tiết có tại `results/kiet/demo_report.json` sau khi chạy demo.

## Giới hạn

Chưa ghép bộ lọc, Sobel, pipeline hoặc bố cục giao diện. Callback mở/lưu đã
có logic và kiểm thử giả lập, chưa kiểm tra nút bấm trên ứng dụng hoàn chỉnh.
Chưa đánh giá ảnh tự nhiên, ảnh tối, nhiễu, nhiều chi tiết và thời gian toàn
luồng. Nhóm thực hiện sau tích hợp, chỉ đưa số liệu thực vào báo cáo cuối.
