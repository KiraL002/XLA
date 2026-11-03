# Phân công và sản phẩm bàn giao

Mỗi người phụ trách mã, kiểm thử, thực nghiệm, báo cáo và slide tương ứng cụm
chức năng của mình. Các phần chuyên môn dưới đây hiện chưa được triển khai.

## Hiếu

- Viết `processing/filters.py`: lọc trung bình và xử lý rìa ảnh.
- Bổ sung tham chiếu bộ lọc vào `evaluation/reference.py` theo lượt ghép.
- Viết `evaluation/benchmark.py`, kiểm tra k=3/5 và đo thời gian.
- Bổ sung `tests/test_filters.py`, ví dụ tính tay và kết quả ảnh thực.
- Cập nhật thư viện và hướng dẫn khi cần; viết phần lý thuyết, thực nghiệm và
  slide về làm mịn, xử lý rìa, thời gian.

## Long

- Viết `processing/edges.py`: Sobel và độ lớn gradient.
- Triển khai `pipeline.py`, bố cục `ui.py`; hoàn thiện `main.py` khi có giao diện.
- Thống nhất hàm sự kiện với Kiệt để nối mở/lưu, xử lý và thông báo lỗi.
- Bổ sung nhánh Sobel tham chiếu, ghép nhánh tham chiếu và kiểm thử tích hợp.
- Viết `tests/test_edges.py`, phối hợp `tests/test_pipeline.py`; viết báo cáo,
  slide về Sobel, kiến trúc và trường hợp thất bại.

## Kiệt

- Viết `image_io.py`, `processing/grayscale.py`, `processing/sketch.py`.
- Nối mở/lưu và thông báo lỗi vào giao diện sau khi thống nhất sự kiện với Long.
- Bổ sung tham chiếu mức xám; kiểm thử đầu vào, mức xám, ngưỡng, tranh và lưu PNG.
- Bổ sung `tests/test_grayscale.py`, `tests/test_sketch.py`, `tests/test_image_io.py`.
- Viết phần đầu vào/đầu ra, mức xám, tạo tranh, kết quả kiểm thử và slide/demo
  tương ứng.

## Chung

- Chọn ảnh, ghi nguồn, tách nhóm chọn tham số và nhóm đánh giá.
- Đọc `INTERFACES.md` trước khi code; không đổi tên hàm hoặc kiểu dữ liệu riêng lẻ.
- Mỗi người cung cấp cách chạy lại, ảnh và bảng đo thực tế của mình.
- Ghép thử định kỳ; cùng rà báo cáo, slide và tập trả lời về toàn bộ luồng.
- Ghi đóng góp theo công việc thực tế; không coi việc tạo bộ khung là thuật toán
  hoặc thực nghiệm đã hoàn thành.
