# Kết quả chạy

Chạy từ thư mục dự án:

```powershell
.\.venv\Scripts\python.exe -m tools.evaluate_sketch
```

`sketch_evaluation/` nhận bảng đối chiếu OpenCV và ảnh minh họa các bước,
làm mảnh nét, tranh chì có sắc độ. Các tệp sinh ra được bỏ qua bởi Git.

Lệnh `python -m tools.prepare_test_data` tạo lại bộ ảnh thử và lưu ảnh tổng
hợp bộ dữ liệu trong `dataset/`.
