# Hệ thống chuyển ảnh thành tranh vẽ bằng các kỹ thuật xử lý ảnh truyền thống

Nhóm: **Hiếu, Long và Kiệt**. Dự án Python cho bài tập lớn môn Xử lý ảnh.

## Trạng thái hiện tại

**Đã triển khai phần Kiệt**: đọc/lưu, mức xám, phân ngưỡng, tạo tranh, tham chiếu
mức xám OpenCV, hàm mở/lưu bằng hộp thoại và các kiểm thử tương ứng.
Xem [hướng dẫn chạy riêng](docs/KIET_HUONG_DAN.md),
[kết quả kiểm thử](docs/KIET_KET_QUA_KIEM_THU.md) và
[nội dung báo cáo, thuyết trình](docs/KIET_BAO_CAO_VA_THUYET_TRINH.md).

Đã chuẩn bị thêm bộ 18 ảnh có nguồn, kết quả mức xám, bảng theo dõi tích hợp
và tài liệu luyện bảo vệ: [bắt đầu tại đây](docs/KIET_CHUAN_BI_TRONG_KHI_CHO.md).

Lọc trung bình, Sobel, bộ điều phối, công cụ đo và bố cục giao diện vẫn là bộ
khung. Chưa có ứng dụng chạy toàn luồng; `--gui` vẫn báo chưa triển khai.

Luồng dự kiến: **RGB → mức xám → lọc trung bình → Sobel → phân ngưỡng → tranh nét**.
Thuật toán chính tự viết bằng NumPy; OpenCV phục vụ nhánh đối chiếu.

## Cài đặt trên Windows trong PowerShell

Mở thư mục `D:\XLA\tranh_ve` trong VS Code. Dùng Python 3.10 trở lên có Tkinter;
NumPy, Pillow và OpenCV cần có bản tương thích với phiên bản Python được chọn.

```powershell
Set-Location D:\XLA\tranh_ve
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe main.py --check
.\.venv\Scripts\python.exe main.py --check-deps
```

Gọi trực tiếp Python trong `.venv` giúp không cần đổi execution policy để kích
hoạt môi trường. Trong VS Code, dùng **Python: Select Interpreter** để chọn
`.venv\Scripts\python.exe`. Thư viện được liệt kê chưa khóa phiên bản; sau khi
chọn được môi trường chung và kiểm tra đầy đủ, nhóm ghi lại phiên bản đã dùng.
Phần Kiệt đã chạy trên Python 3.12.14; có thể cài bằng
`python -m pip install -r requirements-kiet-tested.txt` để tái hiện phiên bản.

Nếu đã kích hoạt đúng môi trường, có thể dùng `python` thay đường dẫn đầy đủ.
Nếu thiếu `py`, dùng `python -m venv .venv`. Nếu thiếu `tkinter`, kiểm tra thành
phần Tcl/Tk trong bộ cài Python; không cài `tkinter` bằng pip.

## Lệnh hiện có

| Lệnh | Ý nghĩa ở giai đoạn bộ khung |
| --- | --- |
| `python main.py` | In tên đề tài, trạng thái và hướng dẫn |
| `python main.py --check` | Nhập module, kiểm tra các hàm đã khai báo; không gọi thuật toán |
| `python main.py --check-deps` | Kiểm tra NumPy, Pillow, OpenCV và Tkinter trong môi trường hiện tại |
| `python main.py --gui` | Hiện thông báo chưa triển khai, mã thoát 2; chưa mở giao diện |

Mã thoát `0` của `--check` chỉ xác nhận việc nhập module/tên hàm. Nó không có
nghĩa ứng dụng chuyển ảnh đã hoạt động. Mã thoát `1` báo lỗi kiểm tra hoặc thiếu
thư viện. Các module chưa cài đặt vẫn báo `NotImplementedError`.

Chạy kiểm thử phần Kiệt:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Demo phân ngưỡng trên ma trận số, chưa tính biên từ ảnh:

```powershell
.\.venv\Scripts\python.exe demo_kiet.py --magnitude data/test_matrices/threshold_3x5.csv
```

## Cấu trúc

```text
tranh_ve/
  main.py                  Điểm chạy và kiểm tra bộ khung
  ui.py                    Khung giao diện và hàm hộp thoại mở/lưu
  image_io.py              Đọc/lưu ảnh đã triển khai
  pipeline.py              Khai báo bộ điều phối và PipelineResult
  processing/
    __init__.py
    grayscale.py           Chuyển mức xám
    filters.py             Lọc trung bình
    edges.py               Sobel
    sketch.py              Phân ngưỡng và tạo tranh
  evaluation/
    __init__.py
    reference.py           Nhánh OpenCV tham chiếu
    benchmark.py           Đo thời gian
  tests/                   Kế hoạch và nơi bổ sung kiểm thử
  data/
    test_matrices/         Ma trận đầu vào có sẵn
    test_images/           Nơi nhóm bổ sung ảnh và ghi nguồn
  results/                 Nơi lưu kết quả thực tế
  docs/
    INTERFACES.md          Quy ước bắt buộc để ghép module
    PHAN_CONG.md           Tệp và nội dung từng thành viên phụ trách
    WORKFLOW.md            Cách làm độc lập và các mốc tích hợp
  requirements.txt
  .gitignore
  README.md
```

## Bắt đầu chia việc

1. Cả nhóm đọc [quy ước hàm](docs/INTERFACES.md).
2. Xem [phân công](docs/PHAN_CONG.md) và [cách phối hợp](docs/WORKFLOW.md).
3. Mỗi người triển khai module của mình và thêm kiểm thử theo `tests/README.md`.
4. Ghép từng phần sớm, giữ nguyên tên hàm, kiểu dữ liệu và khóa `PipelineResult`.

Ảnh giả lập và ma trận số chỉ dùng kiểm tra số học. Kết quả nộp phải đến từ
thuật toán và dữ liệu thực nghiệm của nhóm, có thể chạy lại được.
