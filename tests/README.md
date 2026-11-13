# Kế hoạch kiểm thử

Đã có kiểm thử phần Kiệt: mức xám, tạo tranh, đọc/lưu và hàm hộp thoại.
Lệnh `python main.py --check`
chỉ kiểm tra nhập module và sự tồn tại của tên hàm, không chứng minh thuật toán đúng.

Các phần còn lại bổ sung kiểm thử bằng `unittest` theo phân công:

| Tệp dự kiến | Phụ trách | Các trường hợp cần kiểm tra |
| --- | --- | --- |
| `test_filters.py` | Hiếu | Ảnh hằng, ảnh xung, kết quả tính tay, rìa ảnh, k=3/5, k sai, không sửa đầu vào |
| `test_edges.py` | Long | Ảnh hằng có gradient 0, cạnh ngang/dọc, rìa, ảnh nhỏ, không sửa đầu vào |
| `test_grayscale.py` | Kiệt | Đỏ/xanh lục/xanh lam, trắng/đen, kiểu float32, dữ liệu sai |
| `test_sketch.py` | Kiệt | M nhỏ hơn/bằng/lớn hơn T, bool đầu ra, nét 0/nền 255, tham số sai |
| `test_image_io.py` | Kiệt | Ảnh màu/xám, tệp hỏng, lưu/đọc PNG trong thư mục tạm |
| `test_ui_io.py` | Kiệt | Giả lập chọn/hủy tệp và lỗi đọc/ghi; không tạo cửa sổ |
| `test_pipeline.py` | Long và cả nhóm | Đúng 5 khóa, kích thước và kiểu dữ liệu; chạy toàn luồng sau tích hợp |

Chạy từ thư mục `tranh_ve` sau khi đã thêm kiểm thử:

```powershell
python -m unittest discover -s tests -v
```

Nếu công cụ báo `Ran 0 tests`, nghĩa là chưa có ca kiểm thử, không được ghi rằng
thuật toán đã kiểm thử thành công. Dữ liệu đầu vào số học nằm ở
`data/test_matrices/`; các kỳ vọng cơ bản được ghi trong README của thư mục đó.
