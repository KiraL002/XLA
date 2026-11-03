# Ma trận đầu vào dùng kiểm thử độc lập

Đây là dữ liệu tạo có chủ đích để kiểm tra số học, không phải kết quả thực nghiệm.
Mỗi tệp CSV là một mảng mức xám 2 chiều, không có dòng tiêu đề.

Đọc khi đang ở thư mục `tranh_ve`:

```python
import numpy as np

gray = np.loadtxt("data/test_matrices/constant_5x5.csv", delimiter=",", dtype=np.float32)
```

| Tệp | Mục đích và kỳ vọng cần kiểm tra sau khi triển khai |
| --- | --- |
| `constant_5x5.csv` | Mọi điểm bằng 80; lọc trung bình giữ 80; Sobel bằng 0 |
| `impulse_5x5.csv` | Một điểm 255 giữa nền 0; dùng tính tay các ô của bộ lọc |
| `vertical_edge_7x7.csv` | Cạnh dọc, chủ yếu đáp ứng Gx theo kernel thống nhất |
| `horizontal_edge_7x7.csv` | Cạnh ngang, chủ yếu đáp ứng Gy theo kernel thống nhất |

Hiếu và Long có thể đọc trực tiếp các mảng này để làm việc, không cần chờ hàm
đọc ảnh hoặc hàm mức xám. Kiệt có thể tự tạo mảng RGB nhỏ và mảng độ lớn gradient
trong tệp kiểm thử mà không cần chờ Sobel.

Ví dụ quy tắc đã thống nhất cho bước tạo tranh: với M = [0, 100, 101], T = 100,
mặt nạ là [False, False, True], tranh là [255, 255, 0]. Đây là kỳ vọng tính tay.
Khi viết kiểm thử, đặt các giá trị này trong mảng 2 chiều theo giao tiếp hàm.
