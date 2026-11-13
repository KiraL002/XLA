# Ảnh thử của nhóm

Đã có 18 ảnh: 6 ảnh chụp gốc công khai và 12 biến thể kiểm soát. Không gọi đây
là 18 cảnh độc lập hoặc ảnh do nhóm tự chụp. Gồm chân dung, cốc cà phê, cỏ,
mèo, người chụp ảnh và tên lửa ngoài trời; có bản tối, sáng, nhiễu và thu nhỏ.

Mỗi ảnh có nguồn, tác giả/ghi công, thông tin sử dụng, cách biến đổi, kích thước,
SHA256 và seed trong `manifest.csv`. Ba ảnh gốc astronaut/coffee/grass cùng
các biến thể thuộc tuning (9 ảnh); chelsea/camera/rocket thuộc evaluation (9 ảnh).
Các biến thể của một ảnh luôn cùng nhóm. Không có dữ liệu huấn luyện mô hình.

Tuning dùng chọn k/T sau khi có pipeline; evaluation dùng đánh giá cấu hình
đã chốt. Việc kiểm tra mức xám trên cả 18 ảnh không chọn k/T và không là đánh
giá toàn hệ thống. Tránh điều chỉnh cấu hình dựa vào ảnh evaluation.

Nguồn gốc và ghi công tại `data/source_images/SOURCES.md` và `sources.json`.
Tệp ảnh gốc được kiểm SHA256 theo registry scikit-image v0.25.2 trước khi tạo
biến thể. Sáng/tối và nhiễu là biến đổi số để kiểm thử, không phải ảnh chụp
trong điều kiện khác. Công thức và seed giúp chạy lại được.

Tái tạo offline từ sáu ảnh đã tải (ghi lại các biến thể và manifest):

```powershell
.\.venv\Scripts\python.exe -m tools.prepare_test_data
```

Chỉ dùng `--download` nếu cần tải lại dữ liệu qua Internet. Script không cần
cài scikit-image, chỉ dùng NumPy/Pillow và thư viện chuẩn.

Không dùng ảnh kết quả trong báo cáo tham khảo làm kết quả của nhóm.
