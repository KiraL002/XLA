# Làm việc song song

## Việc cần thống nhất trước

1. Mọi người dùng cùng bản bộ khung và đọc `INTERFACES.md`.
2. Mỗi người tạo môi trường ảo, cài requirements và chạy lệnh kiểm tra.
3. Chốt tệp phụ trách và lịch ghép, chọn ảnh dùng chung.

## Việc có thể làm độc lập

- Hiếu dùng ma trận trong `data/test_matrices/` để viết và kiểm tra bộ lọc.
- Long dùng ảnh cạnh trong cùng thư mục để viết và kiểm tra Sobel; dựng bố cục UI.
- Kiệt dùng mảng RGB và mặt nạ mẫu tự tạo trong kiểm thử để viết mức xám,
  phân ngưỡng, tạo tranh; dùng ảnh thật để phát triển đọc/lưu.

Không cần chờ `load_rgb`, `to_grayscale` hoặc Sobel hoàn thành mới làm module khác.
Không gọi toàn pipeline để kiểm tra một module chưa có đủ các bước phụ thuộc.
Đọc CSV bằng NumPy là nạp dữ liệu thử, không dùng thay cho hàm đọc ảnh của sản phẩm.

## Mốc tích hợp

1. Ghép mức xám + làm mịn + Sobel, kiểm tra dạng mảng và kiểu dữ liệu.
2. Ghép phân ngưỡng + tạo tranh; chạy từ đọc ảnh đến lưu PNG.
3. Nối UI, đối chiếu OpenCV và chạy bộ ảnh chung; đo, ghi kết quả thật.

Nếu module chưa xong, để `NotImplementedError` hiện rõ hoặc dùng dữ liệu thử
trong kiểm thử riêng. Không trả ảnh giả rồi báo luồng xử lý đã hoàn thành.

## Quản lý thay đổi

Có thể dùng kho Git chung với các nhánh `hieu-filters`, `long-edges-ui`,
`kiet-io-sketch`. Kho `KiraL002/XLA` đã có bộ khung; phần Kiệt đang phát triển
ở nhánh `kiet-io-sketch`.
Không chia sẻ thư mục `.venv`; mỗi máy tự cài theo requirements.

Mỗi lần bàn giao cần ghi tệp sửa, cách chạy thử, kết quả thực và vấn đề còn lại.
`ui.py`, `main.py` và `evaluation/reference.py` là các tệp có thể cùng liên quan:
thống nhất lượt sửa/ghép để tránh ghi đè. Thay đổi hợp đồng hàm phải được cả nhóm biết.
