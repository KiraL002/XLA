# Nội dung báo cáo và thuyết trình phần Kiệt

Cập nhật 06/11/2026: đã có bộ ảnh và thực nghiệm mức xám mới tại
`KIET_THUC_NGHIEM_ANH_THAT.md`; kịch bản có số liệu thực tại `KIET_ON_TAP_VA_DEMO.md`.

## Đầu vào và đầu ra

Hệ thống tiếp nhận JPEG/PNG, đưa về mảng RGB uint8 gồm ba kênh màu. Module đọc
ảnh sửa hướng theo EXIF và đặt vùng trong suốt trên nền trắng. Mảng trả về tồn
tại độc lập với tệp, có thể truyền sang các module xử lý sau khi đóng tệp.

Tranh đầu ra là ảnh một kênh uint8 có hai mức 0 và 255. Mức 0 biểu diễn nét,
255 biểu diễn nền. Định dạng PNG giúp bảo toàn hai mức này khi lưu. Kích thước
được giữ theo mặt nạ đầu vào của bước tạo tranh.

## Chuyển đổi mức xám

Tại mỗi điểm, tính `Y(x,y) = 0.299R(x,y) + 0.587G(x,y) + 0.114B(x,y)`.
Đổi dữ liệu sang float32 trước khi tính để giữ phần thập phân cho bước làm mịn.
Phương pháp được cài bằng phép toán mảng NumPy; số phép tính tăng tuyến tính
theo số điểm ảnh. Nhánh chính không gọi hàm chuyển mức xám có sẵn.

Nhánh tham chiếu sử dụng OpenCV COLOR_RGB2GRAY trên RGB float32, cùng miền
0–255. Sai khác nhỏ có thể phát sinh do thứ tự phép toán số thực. Đo sai số
giữa hai nhánh kiểm tra độ khớp cài đặt, không đánh giá độ đẹp của tranh.

## Phân ngưỡng và tạo tranh

Với độ lớn gradient M từ Sobel, tạo mặt nạ E bằng phép so sánh `M > T`.
Điểm bằng ngưỡng không được chọn. Hàm nhận gradient thô, không dùng ảnh đã
chuẩn hóa để hiển thị. Giá trị T=100 là cấu hình khởi đầu, chưa phải giá trị
tối ưu thực nghiệm. Khi giảm T, ảnh có thể nhiều nét nhỏ và nhiễu hơn.

Đổi True thành 0 và False thành 255 để tạo tranh nét đen trên nền trắng.
Đầu ra thể hiện đường nét, chưa tái hiện chất liệu giấy hoặc chuyển sắc chì.

## Kiểm thử và phạm vi kết luận

Các kiểm tra bao gồm RGB cơ bản tính tay, đối chiếu OpenCV, giá trị dưới/bằng/
trên ngưỡng, kiểu và kích thước, JPEG/PNG/xám, EXIF, vùng trong suốt, tệp hỏng,
lưu đọc lại PNG, và mô phỏng lỗi ghi để kiểm tra tệp cũ được bảo toàn.
Hộp thoại được kiểm tra bằng giả lập các thao tác chọn, hủy và lỗi đọc/ghi.

Kết quả thực chạy và môi trường được ghi trong `KIET_KET_QUA_KIEM_THU.md`.
Kết luận chỉ áp dụng phần đã kiểm tra. Chưa có thực nghiệm toàn hệ thống cho
tới khi bộ lọc, Sobel và giao diện được ghép và chạy trên ảnh của nhóm.

## Gợi ý ba slide

1. **Đầu vào và mức xám**: RGB, công thức, ví dụ đỏ cho 76.245, lý do giữ float32.
2. **Phân ngưỡng và tạo tranh**: M → E → tranh; T=100, M=100 không là biên,
   M=101 là biên; True thành nét đen 0.
3. **Đọc lưu và kiểm thử**: PNG bảo toàn 0/255, xử lý hủy/lỗi, kết quả thực chạy
   và phần cần kiểm tra sau tích hợp.

## Kịch bản nói khoảng ba phút

“Em phụ trách chuẩn hóa đầu vào, chuyển mức xám và tạo tranh sau khi có độ lớn
gradient. Ảnh được đưa về RGB để các module sử dụng cùng thứ tự kênh. Nếu
nhầm RGB với BGR, trọng số đỏ và xanh lam sẽ bị áp dụng sai.

Em dùng tổng có trọng số: đỏ 0.299, xanh lục 0.587 và xanh lam 0.114. Kết quả
giữ float32 để bước sau nhận giá trị chưa làm tròn. Nhánh OpenCV chỉ dùng
đối chiếu phần tự cài đặt trên cùng miền giá trị.

Sau Sobel, em so sánh độ lớn gradient trực tiếp với ngưỡng. Khi T bằng 100,
M bằng 100 không được lấy, M bằng 101 được lấy. Mặt nạ được đổi thành nét đen
và nền trắng, tạo đầu ra chỉ có hai giá trị.

Em lưu PNG để tránh mất dữ liệu do JPEG. Trước khi ghi, chương trình kiểm tra
dạng mảng và các mức 0/255. Ghi qua tệp tạm giúp lỗi ghi không làm hỏng kết quả
cũ. Em kiểm tra đầu vào hợp lệ, dữ liệu sai, hủy chọn tệp và lỗi đọc ghi.
Hàm mở/lưu đã sẵn sàng để ghép với giao diện chung; chất lượng tranh toàn hệ
thống sẽ được đánh giá sau khi hoàn tất tích hợp.”

Điều chỉnh trạng thái tích hợp và ảnh demo theo thực tế khi bảo vệ.

## Câu hỏi cần hiểu

- **Vì sao không chia đều ba kênh?** Nhóm dùng công thức có trọng số đã thống
  nhất; trung bình cộng tạo một phép chuyển khác và khó đối chiếu cùng cấu hình.
- **Vì sao không ép uint8 ngay?** Ép sớm làm mất phần thập phân trước khi lọc.
- **Vì sao M có thể hơn 255?** M là độ lớn đạo hàm, không phải mức sáng.
- **Vì sao PNG?** PNG giữ chính xác ảnh nhị phân; JPEG có thể sinh mức trung gian.
- **Bấm hủy có xóa ảnh cũ không?** Hàm trả None/False; UI chỉ đổi ảnh khi mở thành công.
- **Khớp OpenCV chứng minh tranh đẹp không?** Không; thẩm mỹ cần ảnh thật và đánh giá sau tích hợp.
