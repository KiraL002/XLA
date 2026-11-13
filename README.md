# Hệ thống chuyển ảnh thành tranh vẽ bằng các kỹ thuật xử lý ảnh truyền thống

Nhóm: **Hiếu, Long và Kiệt**. Dự án Python cho bài tập lớn môn Xử lý ảnh.

Ứng dụng đã ghép phần đọc/lưu của Kiệt, bộ lọc trung bình của Hiếu và Sobel,
pipeline cùng giao diện Tkinter của Long. Mở ảnh JPG/PNG, chọn cửa sổ lọc
và ngưỡng, bấm **Xử lý**, chọn bước cần xem rồi bấm **Lưu tranh (PNG)**.
Sau khi đổi ảnh hoặc tham số, bấm **Xử lý** để tạo kết quả mới.

**RGB → mức xám → lọc trung bình → Sobel → phân ngưỡng → tranh nét**

Thuật toán chính dùng NumPy. Nhánh OpenCV dùng để đối chiếu. Bộ 18 ảnh,
thông tin nguồn và kế hoạch kiểm thử có trong
[tài liệu chuẩn bị](docs/KIET_CHUAN_BI_TRONG_KHI_CHO.md).

## Cài đặt trên Windows trong PowerShell

Mở thư mục `D:\XLA\tranh_ve` trong VS Code. Dùng Python 3.10 trở lên có Tkinter;
NumPy, Pillow và OpenCV cần có bản tương thích với phiên bản Python được chọn.

```powershell
Set-Location D:\XLA\tranh_ve
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --gui
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

| Lệnh | Tác dụng |
| --- | --- |
| `python main.py` | In tên đề tài, trạng thái và hướng dẫn |
| `python main.py --check` | Nhập module, kiểm tra các hàm đã khai báo; không gọi thuật toán |
| `python main.py --check-deps` | Kiểm tra NumPy, Pillow, OpenCV và Tkinter trong môi trường hiện tại |
| `python main.py --gui` | Mở cửa sổ chuyển ảnh thành tranh nét |

Mã thoát `0` của `--check` xác nhận việc nhập module và tên hàm.
Mã thoát `1` báo lỗi kiểm tra hoặc thiếu thư viện.

Chạy bộ kiểm thử của cả nhóm.

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
  main.py                  Điểm chạy và kiểm tra môi trường
  ui.py                    Giao diện Tkinter và hộp thoại mở/lưu
  image_io.py              Đọc/lưu ảnh đã triển khai
  pipeline.py              Luồng xử lý và PipelineResult
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
  tests/                   Kiểm thử của cả nhóm
  data/
    test_matrices/         Ma trận đầu vào có sẵn
    test_images/           Ảnh kiểm thử và manifest nguồn
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
