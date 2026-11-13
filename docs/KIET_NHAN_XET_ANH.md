# Nhận xét quan sát mức xám và giả thuyết cần kiểm tra sau tích hợp

Đã quan sát hai bảng ảnh tổng hợp ngày 06/11/2026: ảnh đầu vào và ảnh mức xám
tại `results/kiet_preparation/`. Các nhận xét dưới đây chỉ nói về các ảnh này,
chưa khẳng định chất lượng tranh hoặc độ chính xác biên của Sobel.

## Những gì đã nhìn thấy

- Chân dung I01 và bản xám vẫn thể hiện cùng khuôn mặt, bộ đồ và vật thể nền.
  Bản I02 tối đi rõ; mức xám trung bình giảm từ 115.406 xuống 40.390.
- Cốc cà phê I04 còn nhận ra cốc, đĩa, thìa và vân gỗ ở bản xám. I05 có vùng
  sáng lớn hơn, với mức xám trung bình 167.458 so với 103.643 của bản gốc.
- Ảnh cỏ I07 và người chụp ảnh I13 vốn là ảnh xám. Nạp thành RGB rồi chuyển
  xám vẫn giữ cùng nội dung; sai số float32 có thể rất nhỏ thay vì đúng 0.
- I11 thể hiện các chấm muối tiêu trên lông và vùng nền của ảnh mèo.
  I12 tối đi rõ; trung bình mức xám 41.814 so với 119.467 của I10.
- Ảnh tên lửa I16 có bầu trời tối và đèn sáng. I17 tối hơn, trung bình giảm
  từ 60.986 xuống 21.345. Chuyển xám không tự làm sáng hoặc khôi phục chi tiết.
- Các bản thu nhỏ giữ nội dung chung; kích thước thật được ghi trong manifest,
  không đánh giá độ phân giải chỉ qua thumbnail cùng kích thước hiển thị.

Các số trên làm tròn từ bảng thực chạy trong `KIET_THUC_NGHIEM_ANH_THAT.md`.
Kiểm tra tự động trên 18 ảnh không phát hiện lỗi dạng mảng, kiểu dữ liệu,
miền giá trị, sửa ảnh đầu vào hoặc sai khác vượt ngưỡng so với OpenCV.

## Giả thuyết và phép thử cần làm sau khi ghép

| Ảnh/điều kiện | Giả thuyết chưa xác nhận bằng tranh | Cách kiểm tra |
| --- | --- | --- |
| Cỏ, lông mèo, nền nhiều chi tiết | Có thể sinh quá nhiều nét kết cấu | So tranh ở các T trên tuning, ghi nét thừa/mất |
| Ảnh tối | Có thể khó giữ các nét yếu với T cố định | So với ảnh gốc cùng nhóm, giữ k/T nhất quán |
| Muối tiêu/Gaussian | Có thể xuất hiện biên giả; mean filter chưa chắc xử lý tốt muối tiêu | So trước/sau lọc, k=3 và 5 trên tuning |
| Quá sáng | Vùng bị cắt về 255 có thể mất chi tiết | So ảnh sáng và gốc; xem vùng trắng rộng |
| Thu nhỏ | Nét nhỏ có thể biến mất | Kiểm kích thước, xem tranh thực thay vì chỉ thumbnail |

Không điền các giả thuyết này vào cột “Thực tế” như thể đã chạy. Sau tích hợp,
thay bằng quan sát cụ thể và lưu ảnh minh chứng, kể cả kết quả không tốt.
