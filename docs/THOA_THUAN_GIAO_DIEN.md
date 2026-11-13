# Đặc tả mở ảnh xử lý và lưu để ghép giao diện

Đây là tài liệu bàn giao để nhóm rà soát khi Long làm bố cục, chưa phải xác
nhận đã trao đổi hoặc đã ghép giao diện. Kiệt phụ trách đọc/lưu và callback;
Long phụ trách cửa sổ, trạng thái, vùng hiển thị và gọi pipeline.

## Trạng thái và thao tác

| Thời điểm | Trạng thái dữ liệu | Hành vi cần có |
| --- | --- | --- |
| Khởi động | current_rgb=None, current_sketch=None | Chưa cho xử lý/lưu, hoặc hiển thị thông báo phù hợp |
| Mở thành công | Thay current_rgb; current_sketch=None | Hiện ảnh mới, bỏ kết quả cũ, đánh dấu cần xử lý |
| Hủy mở hoặc mở lỗi | Giữ nguyên ảnh và tranh cũ | Không xóa trạng thái đang có; lỗi đọc được callback thông báo |
| Đổi k/T | Đánh dấu kết quả cũ không còn đúng cấu hình | Yêu cầu xử lý lại trước khi lưu; không gắn nhãn tham số mới cho tranh cũ |
| Xử lý thành công | Lưu đủ 5 khóa PipelineResult | Cập nhật ảnh trung gian, tranh gốc, tham số của lần chạy |
| Xử lý thất bại | Không coi kết quả cũ là kết quả mới | Báo lỗi; không mở hộp lưu với nhãn lần chạy thất bại |
| Lưu thành công | Giữ ảnh/tranh đang có | Chỉ báo thành công sau khi save_sketch_dialog trả True |
| Hủy lưu hoặc lưu lỗi | Giữ dữ liệu đang có | Không báo thành công; tệp cũ không bị hỏng khi ghi thất bại |

Nếu đổi tham số rồi đổi lại, cách đơn giản là yêu cầu bấm Xử lý lại. Nhóm có
thể tối ưu sau nhưng cần giữ rõ cấu hình nào đã sinh tranh đang hiển thị.

## Giao tiếp đã có

```python
candidate = open_image_dialog(root)
if candidate is not None:
    current_rgb = candidate
    current_sketch = None
    # Long cập nhật preview và trạng thái nút.

# Sau khi pipeline hoàn thành thành công:
current_sketch = result['sketch']

# Sự kiện Lưu nhận tranh gốc, không nhận preview đã thu nhỏ:
saved = save_sketch_dialog(current_sketch, root)
```

`root` là cửa sổ Tkinter đang tồn tại. Callback không tạo cửa sổ chính và
không biết cách bố trí label/widget. Giao diện giữ tham chiếu PhotoImage khi
hiển thị và không ghi đè mảng tính toán bằng ảnh xem trước.

## Tham số và dữ liệu

- k chỉ nhận số nguyên 3 hoặc 5; T phải hữu hạn, không âm; so sánh M > T.
- Kiểm tra chuỗi nhập trước khi gọi pipeline. Không chấp nhận NaN/vô cực.
- RGB là uint8 H×W×3; ảnh xám float32; mask bool; tranh uint8 chỉ 0/255.
- Bản hiển thị gradient có thể chuẩn hóa riêng, nhưng phân ngưỡng phải dùng
  gradient thô. Khi lưu giữ kích thước tranh, không dùng kích thước ô preview.

## Các ca kiểm tra thủ công sau khi ghép

Các ca này nằm trong bảng theo dõi Excel, tab Giao_dien. Tất cả đang Chưa chạy:

1. Khởi động chưa có ảnh, thử Xử lý và Lưu.
2. Mở ảnh hợp lệ, xác nhận RGB và preview.
3. Hủy mở khi đang có ảnh/tranh; dữ liệu cũ giữ nguyên.
4. Mở tệp hỏng; báo lỗi, không mất dữ liệu cũ.
5. Đổi sang ảnh mới sau khi đã có tranh; không lưu nhầm tranh cũ.
6. Nhập k/T không hợp lệ, kể cả NaN và vô cực; báo lỗi rõ.
7. Đổi k/T sau xử lý; yêu cầu tạo lại kết quả trước khi lưu.
8. Xử lý hợp lệ; hiện đủ trung gian, kết quả đúng dtype/shape.
9. Preview thu nhỏ nhưng tranh lưu giữ kích thước xử lý gốc.
10. Lưu PNG thành công, đọc lại có đúng 0/255; chỉ báo thành công sau ghi.
11. Hủy lưu; không tạo tệp và không báo thành công.
12. Lưu vào nơi không ghi được; báo lỗi, không làm hỏng tệp cũ.

Kiểm thử callback bằng mock trước đây đã đạt, nhưng không thay thế các ca
kiểm tra thủ công trên giao diện thật. Ghi kết quả và người thử khi thực hiện.
