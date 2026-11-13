# Quy ước giao tiếp chung

Tài liệu này mô tả hợp đồng chung. Phần Kiệt đã triển khai kiểm tra dữ liệu;
các phần còn lại giữ `NotImplementedError` đến khi được cài đặt.

## Dữ liệu và tham số

- Ảnh RGB: mảng NumPy `(H, W, 3)`, `uint8`, thứ tự **RGB**, không phải BGR.
- Ảnh mức xám và ảnh làm mịn: `(H, W)`, `float32`, hữu hạn trong `[0, 255]`.
- Độ lớn gradient: `(H, W)`, `float32`, hữu hạn và không âm; có thể lớn hơn 255.
- Mặt nạ biên: `(H, W)`, `bool`; `True` là nét.
- Tranh cuối: `(H, W)`, `uint8`; nét đen `0`, nền trắng `255`.
- `H` và `W` phải dương. Các hàm giữ nguyên kích thước và không sửa đầu vào.
- `ksize` chỉ nhận số nguyên `3` hoặc `5`; `threshold` nhận số hữu hạn không âm.
- Bù rìa bằng lặp điểm rìa: `np.pad(..., mode="edge")`. Nhánh OpenCV dùng
  `BORDER_REPLICATE`. Ảnh nhỏ hơn kernel vẫn giữ kích thước nhờ bù rìa.
- Đầu vào sai hợp đồng báo `ValueError`. Lỗi đọc/lưu tệp được truyền cho mã gọi;
  giao diện tiếp nhận và hiện thông báo. Hàm xử lý không mở hộp thoại.

## Các hàm đã chốt

| Module | Hàm | Đầu ra | Phụ trách |
| --- | --- | --- | --- |
| `image_io.py` | `load_rgb(path)` | RGB `uint8` | Kiệt |
| `image_io.py` | `save_sketch(path, sketch)` | `None`, lưu PNG | Kiệt |
| `processing/grayscale.py` | `to_grayscale(rgb)` | Xám `float32` | Kiệt |
| `processing/filters.py` | `mean_filter(gray, ksize=3)` | Làm mịn `float32` | Hiếu |
| `processing/edges.py` | `sobel_magnitude(gray)` | Độ lớn gradient `float32` | Long |
| `processing/sketch.py` | `threshold_edges(magnitude, threshold=100.0)` | Mặt nạ `bool` | Kiệt |
| `processing/sketch.py` | `render_sketch(edges)` | Tranh `uint8` | Kiệt |
| `pipeline.py` | `run_pipeline(rgb, ksize=3, threshold=100.0)` | `PipelineResult` | Long |
| `ui.py` | `launch_app()` | `None` | Long, Kiệt phối hợp mở/lưu |

`PipelineResult` là từ điển có đúng các khóa:

```text
gray        ảnh mức xám
smooth      ảnh làm mịn
magnitude   độ lớn gradient thô
edges       mặt nạ biên
sketch      tranh cuối
```

## Quy tắc tính toán để tránh khác kết quả

Mức xám dùng trọng số `0.299R + 0.587G + 0.114B`. Giữ giá trị `float32`, không
làm tròn trước khi đưa sang bộ lọc. Bộ lọc trung bình dùng trọng số đều `1/(k*k)`.

Sobel dùng phép tương quan, **không lật kernel**:

```text
Kx = [-1  0  1]      Ky = [-1 -2 -1]
     [-2  0  2]           [ 0  0  0]
     [-1  0  1]           [ 1  2  1]
```

Tính độ lớn bằng `sqrt(Gx**2 + Gy**2)`. Không ép về `uint8`, không chuẩn hóa
riêng từng ảnh trước phân ngưỡng. Nếu cần ảnh xem trước thì tạo bản hiển thị
riêng, giữ nguyên mảng dùng cho tính toán.

Quy tắc phân ngưỡng là `M > T`, không phải `M >= T`. Giá trị `T=100` chỉ là
cấu hình khởi đầu để thử, chưa là tham số tối ưu đã thực nghiệm.

Luồng chạy đã thống nhất:

```text
RGB → to_grayscale → mean_filter → sobel_magnitude
    → threshold_edges → render_sketch
```

## Nhánh đối chiếu

Các hàm `reference_grayscale`, `reference_mean_filter`,
`reference_sobel_magnitude` và `run_reference_pipeline` có trong
`evaluation/reference.py`. Tham số ảnh và kiểu đầu ra tương ứng nhánh chính.
Chỉ nhánh này sử dụng phương thức xử lý ảnh OpenCV.

So riêng bộ lọc phải dùng cùng một ảnh xám `float32`, cùng kernel và quy tắc rìa.
Khi so toàn luồng, ghi rõ nếu chuyển xám bằng OpenCV có sai khác công thức/làm tròn.

`measure_runtime(function, repeats=5, warmup=1)` nhận callable không tham số,
trả `median_ms`, `min_ms`, `max_ms` sau khi triển khai. Không dùng số liệu giả.

Trước khi thay đổi hợp đồng, trao đổi với cả nhóm và cập nhật tài liệu này.

## Hộp thoại mở và lưu để ghép giao diện

- `ui.open_image_dialog(parent)` trả RGB uint8 khi mở thành công, None khi
  hủy/lỗi. UI giữ ảnh cũ nếu nhận None; xóa kết quả cũ khi nhận ảnh mới.
- `ui.save_sketch_dialog(sketch, parent)` trả True khi ghi thành công; False
  khi hủy/lỗi hoặc sketch là None. Truyền tranh gốc, không dùng bản xem trước.
- Hai hàm không tạo cửa sổ chính; Long truyền cửa sổ Tkinter làm parent và
  nối với nút bấm. Lỗi đọc/ghi được hiển thị bằng messagebox.
- Ảnh PNG có alpha được ghép trên nền trắng; EXIF được sửa trước khi trả mảng.
- `reference_grayscale` chuyển RGB thành float32 trước cvtColor, giữ miền
  0–255 để tránh sai khác do ép kết quả xám về uint8.
