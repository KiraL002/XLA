# Hệ thống chuyển ảnh thành tranh vẽ bằng các kỹ thuật xử lý ảnh truyền thống

Dự án Python cho bài tập lớn môn Xử lý ảnh. Ứng dụng dùng Tkinter để mở
ảnh JPG/PNG, xem từng bước xử lý và lưu tranh PNG. Chọn kiểu tranh, cửa sổ
lọc và ngưỡng biên, sau đó bấm **Xử lý**.
Sau khi đổi ảnh hoặc tham số, bấm **Xử lý** để tạo kết quả mới.

**RGB → mức xám → lọc trung bình → Sobel → phân ngưỡng → tranh nét**

Chọn **Làm mảnh nét** rồi bấm **Xử lý** để làm mảnh mặt nạ biên bằng
Zhang–Suen trước khi tạo tranh. Mục **Mặt nạ biên** hiển thị kết quả phân
ngưỡng. Mục **Tranh kết quả** và nút lưu dùng kết quả của tùy chọn đang áp dụng.
Trong kiểu **Tranh nét**, thanh trạng thái cho biết số điểm nét trước và sau
khi làm mảnh.

Trong **Kiểu tranh**, chọn **Tranh chì có sắc độ** rồi bấm **Xử lý**. Chế độ
này lọc trung vị 3×3 trước khi lọc trung bình, dựng bóng bằng hai hướng gạch và
giữ viền nhẹ theo độ lớn Sobel. **Ngưỡng biên** chọn các viền được nhấn đậm.
**Làm mảnh nét** thu hẹp lớp nét nhấn, nên thay đổi ít khi ngưỡng cao và ảnh
có ít nét nhấn. Nút lưu xuất PNG mức xám ở kích thước gốc. **Tranh nét** là
kiểu mặc định.

Thuật toán chính dùng NumPy. Nhánh OpenCV dùng để đối chiếu.
[Bộ ảnh thử](data/test_images/README.md) gồm 18 ảnh kèm thông tin nguồn.

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

Trong VS Code, dùng **Python: Select Interpreter** để chọn
`.venv\Scripts\python.exe`.

Nếu đã kích hoạt đúng môi trường, có thể dùng `python` thay đường dẫn đầy đủ.
Nếu thiếu `py`, dùng `python -m venv .venv`. Nếu thiếu `tkinter`, kiểm tra thành
phần Tcl/Tk trong bộ cài Python; không cài `tkinter` bằng pip.

## Lệnh hiện có

| Lệnh | Tác dụng |
| --- | --- |
| `python main.py` | In tên đề tài, trạng thái và hướng dẫn |
| `python main.py --check` | Nhập module, kiểm tra các hàm đã khai báo; không gọi thuật toán |
| `python main.py --check-deps` | Kiểm tra NumPy, Pillow, OpenCV và Tkinter trong môi trường hiện tại |
| `python main.py --gui` | Mở cửa sổ chuyển ảnh thành tranh vẽ |

Mã thoát `0` của `--check` xác nhận việc nhập module và tên hàm.
Mã thoát `1` báo lỗi kiểm tra hoặc thiếu thư viện.

Chạy bộ kiểm thử của cả nhóm.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Đối chiếu và tạo ảnh minh họa

```powershell
.\.venv\Scripts\python.exe -m tools.evaluate_sketch
```

Lệnh lưu vào `results/sketch_evaluation/`:

- `cac_buoc_xu_ly.png` minh họa từng bước trên ảnh cốc cà phê, kèm tranh OpenCV.
- `so_sanh_lam_manh.png` đặt tranh trước và sau làm mảnh cạnh nhau trên ba ảnh.
- `so_sanh_tranh_chi.png` đối chiếu ảnh gốc, tranh nét và tranh chì trên ba ảnh.
- `doi_chieu_opencv.csv` đối chiếu tranh mặc định trên 18 ảnh, hai cửa sổ lọc
  và ba ngưỡng. Hai nhánh dùng chung cách phân ngưỡng và tạo tranh. Sai số
  gradient và số điểm khác cho biết độ khớp của hai cách cài đặt.

Nguồn ảnh nằm trong `data/test_images/manifest.csv`. Thuật toán làm mảnh dựa
trên [bài báo gốc của Zhang và Suen](https://doi.org/10.1145/357994.358023).

## Cấu trúc

```text
tranh_ve/
  main.py                  Điểm chạy và kiểm tra môi trường
  ui.py                    Giao diện Tkinter và hộp thoại mở/lưu
  image_io.py              Đọc ảnh và lưu tranh PNG
  pipeline.py              Luồng xử lý và PipelineResult
  processing/
    __init__.py
    grayscale.py           Chuyển mức xám
    filters.py             Lọc trung bình và trung vị
    edges.py               Sobel
    sketch.py              Phân ngưỡng, làm mảnh và tạo tranh
  evaluation/
    __init__.py
    reference.py           Nhánh OpenCV tham chiếu
    benchmark.py           Đo thời gian
  tests/                   Kiểm thử của cả nhóm
  data/
    source_images/         Ảnh gốc và thông tin nguồn
    test_matrices/         Ma trận đầu vào có sẵn
    test_images/           Ảnh kiểm thử và manifest nguồn
  tools/                   Tạo bộ ảnh thử và chạy đối chiếu
  results/                 Kết quả sinh từ các công cụ
  docs/
    INTERFACES.md          Quy ước dữ liệu và giao tiếp giữa các module
  requirements.txt
  .gitignore
  README.md
```
