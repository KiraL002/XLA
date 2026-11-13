# Các phần chuẩn bị của Kiệt đã hoàn thành

## Đọc tài liệu nào trước

1. `KIET_THUC_NGHIEM_ANH_THAT.md`: kết quả mức xám thực chạy trên 18 ảnh.
   `KIET_NHAN_XET_ANH.md`: nhận xét ảnh đã quan sát và giả thuyết cho bước tích hợp.
2. `KIET_ON_TAP_VA_DEMO.md`: lệnh demo, bài tập tính tay, kịch bản và câu hỏi.
3. `THOA_THUAN_GIAO_DIEN.md`: đặc tả mở/xử lý/lưu để Long rà soát và ghép.
4. `../outputs/kiet_preparation/Theo_doi_kiem_thu_XLA.xlsx`: bảng ghi kết quả
   tích hợp, giao diện, mức xám đã chạy và thông tin nguồn ảnh.

## Đã có sẵn

- 18 ảnh trong `data/test_images/`, manifest có nguồn, ghi công, nhóm và mã băm.
- 6 nguồn gốc độc lập tại `data/source_images/`, đã xác minh registry SHA256.
- Nhóm tuning/evaluation: 9/9 ảnh, chia theo ảnh gốc, không dùng để training.
- Biến thể tối, sáng, Gaussian, muối tiêu và thu nhỏ có công thức/seed rõ ràng.
- 18 kết quả mức xám, bản xem trước và dữ liệu float32 tại `results/kiet_preparation/`.
- 63 ca thử tích hợp: 54 ca tuning cho k=3/5 và T=50/100/150; 9 ca evaluation
  để trống k/T cho tới khi cấu hình được chốt từ tuning.
- 12 ca giao diện cần chạy thủ công sau khi Long hoàn thiện bố cục.
- Kịch bản nói khoảng ba phút, ví dụ tính tay và 18 câu hỏi luyện bảo vệ.

## Chạy lại những phần đã làm được

```powershell
cd D:\XLA\tranh_ve
.\.venv\Scripts\python.exe -m tools.evaluate_kiet_dataset
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Script đánh giá chỉ chạy phần của Kiệt. Nó ghi lại kết quả mức xám và báo cáo;
không thay phần lọc/Sobel của hai thành viên khác. CSV kế hoạch tích hợp đã
có thì không bị ghi đè. File Excel là bản chụp dữ liệu ngày 06/11/2026; các ô
tiến độ cập nhật bằng công thức khi nhập trạng thái, nhưng không tự đọc lại
CSV/JSON khi chạy script. Dùng cùng một file theo dõi chính để tránh lệch bản.

## Sau khi nhóm bàn giao

1. Long và Kiệt rà quy tắc trạng thái trong `THOA_THUAN_GIAO_DIEN.md`.
2. Ghép và chạy 54 ca tuning, ghi nhận thực tế, kiểm tra kiểu/kích thước và nét.
3. Chọn một cặp k/T, ghi lý do và đóng băng cấu hình trước khi chạy 9 ca evaluation.
4. Điền thời gian/MAE/tỷ lệ điểm khác chỉ sau khi đo; để trống khi chưa đo,
   không thay bằng 0. Tỷ lệ điểm khác phải dùng cùng pipeline và tham số tham chiếu.
5. Chạy 12 ca giao diện trên cửa sổ thật; mock callback trước đây không thay thế thao tác này.

Các tài liệu bàn giao đã chuẩn bị để nhóm đọc; chưa có trao đổi hay xác nhận
thay cho Long/Hiếu. Kiệt vẫn cần tự thực hành và luyện nói để bảo vệ được mã.
