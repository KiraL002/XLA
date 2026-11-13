# Luyện bảo vệ phần Kiệt

## Bài thực hành cần tự làm

1. Mở `processing/grayscale.py`, giải thích từng kiểm tra đầu vào và công thức.
2. Tính tay RGB [255,0,0] → 76.245, [0,255,0] → 149.685,
   [0,0,255] → 29.07 và [10,20,30] → 18.15.
3. Tính mask từ [0,100,101] khi T=100, rồi tạo tranh [255,255,0].
4. Chạy hai lệnh demo dưới đây, mở PNG và JSON, giải thích đơn vị từng số.
5. Tự nói phần trình bày trong 3 phút và trả lời câu hỏi mà không đọc mã.

Tài liệu đã chuẩn bị giúp luyện tập; chỉ người thực hiện mới xác nhận mình
hiểu và trình bày được. Không ghi việc đã đọc tài liệu là đã làm chủ thuật toán.

## Demo phần đang chạy độc lập

```powershell
cd D:\XLA\tranh_ve
.\.venv\Scripts\python.exe demo_kiet.py --image data/test_images/I04_coffee_original.png --output-dir results/kiet_demo_coffee
.\.venv\Scripts\python.exe demo_kiet.py --magnitude data/test_matrices/threshold_3x5.csv --threshold 100 --output-dir results/kiet_demo_threshold
```

Mở `gray_preview.png` và `demo_report.json` trong thư mục đầu. Giải thích vì
sao bản xem trước uint8 nhưng dữ liệu `gray_float32.npy` giữ phần thập phân.
Trong thư mục sau, tranh 3×5 phải có 5 điểm đen. Đó là demo ma trận, không
được mô tả là ảnh biên Sobel của cốc cà phê.

Khi cả nhóm tích hợp xong, thay phần demo ma trận bằng ảnh thật qua toàn
pipeline; giữ ảnh gốc, trung gian và tranh cuối để trình bày được từng bước.

## Kịch bản khoảng ba phút

“Em phụ trách đọc và lưu ảnh, chuyển mức xám, phân ngưỡng và tạo tranh.
Đầu vào được đưa về RGB uint8 để các module cùng hiểu thứ tự kênh. Ảnh xám
được chuyển về ba kênh khi đọc, và hướng EXIF được xử lý trước khi tạo mảng.

Mức xám được tính từ tổng có trọng số 0.299R, 0.587G và 0.114B. Ví dụ một
điểm đỏ thuần 255 cho mức xám 76.245. Em giữ float32 để bước lọc nhận được
giá trị chưa làm tròn. OpenCV được sử dụng ở nhánh tham chiếu để đối chiếu.

Nhóm đã có 18 ảnh thử từ 6 ảnh nền công khai. Các biến thể sáng, tối, nhiễu
và thu nhỏ được tạo có công thức và seed. 9 ảnh dùng chọn tham số, 9 ảnh dùng
đánh giá; biến thể của cùng một ảnh không bị tách sang hai nhóm. Đây không
phải bộ dữ liệu training vì hệ thống không huấn luyện mô hình.

Sau khi Sobel trả độ lớn gradient M, em chọn điểm có M lớn hơn T. Nếu T=100,
M=100 không là biên, M=101 là biên. True được đổi thành nét đen 0, False thành
nền trắng 255. Tranh được lưu PNG để bảo toàn chính xác hai mức này.

Phần mức xám đã chạy trên đủ 18 ảnh, với sai số lớn nhất so OpenCV khoảng
0.00003052, đạt tiêu chí kiểm tra float32. Chỉ số này cho thấy độ khớp cài
đặt, không chứng minh tranh đẹp. Đánh giá tranh toàn hệ thống cần thực hiện
sau khi ghép bộ lọc, Sobel và giao diện. Các ca thử và ô kết quả đã được chuẩn
bị để nhóm chạy và ghi nhận trung thực.”

## Câu hỏi và câu trả lời cần hiểu

| Câu hỏi | Ý chính để trả lời |
| --- | --- |
| Có cần training? | Không. Công thức cố định; nhóm chỉ hiệu chỉnh k và T. |
| Tại sao chia tuning/evaluation? | Chọn tham số trên một nhóm, kiểm tra cấu hình đã chốt trên nhóm khác. |
| 18 ảnh có độc lập không? | Chỉ 6 ảnh nền độc lập. Các biến thể phụ thuộc nguồn gốc. |
| Tại sao không tách biến thể sang hai nhóm? | Cùng nội dung nền có thể làm đánh giá quá lạc quan. |
| Mức xám là trung bình cộng RGB? | Không; nhóm dùng công thức trọng số đã thống nhất. |
| RGB và BGR khác nhau ở đâu? | Thứ tự đỏ/xanh lam; đọc RGB nhưng áp BGR sẽ dùng sai trọng số. |
| Tại sao float32? | Giữ phần thập phân, nhất quán giao tiếp và đủ cho bài toán. |
| Vì sao không khớp OpenCV tuyệt đối mọi điểm? | Thứ tự phép tính float32 có thể tạo sai khác nhỏ. |
| MAE gần 0 nghĩa là tranh đẹp? | Không. Đây là mức khớp với phép chuyển xám tham chiếu. |
| T=100 và M=100 có phải biên? | Không, vì dùng dấu lớn hơn nghiêm ngặt. |
| Tăng T tác động gì? | Với cùng M, tập biên không tăng; có thể bỏ nét yếu. |
| Vì sao M hơn 255? | M là độ lớn gradient, không phải cường độ điểm ảnh. |
| Vì sao dùng PNG? | Giữ chính xác 0/255, tránh mức trung gian do nén JPEG. |
| Ảnh quá tối đã được cải thiện chưa? | Chưa. Chuyển xám không tự tăng sáng hoặc khôi phục chi tiết. |
| Ảnh nhiều cỏ/lông có thể khó ở đâu? | Có nhiều biên kết cấu. Đây là giả thuyết, cần chạy toàn pipeline xác nhận. |
| Hủy mở ảnh có xóa dữ liệu cũ? | Không; callback trả None, giao diện chỉ cập nhật khi có ảnh hợp lệ. |
| Nếu đổi ảnh hoặc tham số? | Làm mất hiệu lực kết quả cũ, xử lý lại trước khi lưu. |
| Ghi ảnh thất bại có hỏng tệp cũ? | Mã ghi tệp tạm trước; chỉ thay tệp đích khi ghi thành công. |

## Giới hạn cần nói đúng

Các ảnh nguồn có thật, nhưng biến thể tối/sáng/nhiễu là giả lập số có kiểm
soát. Bộ ảnh nhỏ chưa chứng minh tổng quát. Những phát biểu về nét tranh,
chất lượng UI hoặc thời gian toàn pipeline chỉ được đưa ra sau thực nghiệm.
