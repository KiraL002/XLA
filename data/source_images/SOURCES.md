# Nguồn và ghi công ảnh

Sáu ảnh được phân phối trong bộ dữ liệu scikit-image v0.25.2. Đã tải bản cố định
và so SHA256 với registry chính thức. `sources.json` ghi URL tệp, URL tài liệu,
mã băm, tác giả và ngày lấy dữ liệu 06/11/2026. Thông tin sử dụng dưới đây theo
phần Notes của tài liệu scikit-image, không suy ra từ giấy phép mã nguồn thư viện.

| Ảnh gốc | Ghi công | Thông tin sử dụng theo tài liệu | Mô tả nguồn |
| --- | --- | --- | --- |
| astronaut.png | NASA | Public domain | [Astronaut](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.astronaut) |
| coffee.png | Rachel Michetti | CC0 | [Coffee](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.coffee) |
| grass.png | Nguồn DeviantArt qua scikit-image | CC0; bản đã crop và chuyển xám bởi scikit-image | [Grass](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.grass) |
| chelsea.png | Stefan van der Walt | CC0 | [Chelsea](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.chelsea) |
| camera.png | Lav Varshney | CC0 | [Camera](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.camera) |
| rocket.jpg | SpaceX | Public domain theo scikit-image | [Rocket](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.rocket) |

Giữ ghi công này cùng dữ liệu khi chia sẻ với nhóm. Bản original trong bộ
test là PNG được giải mã từ tệp gốc; byte/mã băm có thể khác tệp tải về,
vì vậy manifest ghi cả source_sha256 và sha256.

Registry: https://raw.githubusercontent.com/scikit-image/scikit-image/v0.25.2/skimage/data/_registry.py

## Biến thể do nhóm chuẩn bị

- Tối: round(0.35 × I).
- Sáng: round(clip(1.7 × I + 20, 0, 255)).
- Gaussian: cộng nhiễu N(0,20²), clip và làm tròn; độc lập từng kênh.
- Muối tiêu: xác suất 1.5% điểm đen, 1.5% điểm trắng; chung vị trí giữa các kênh.
- Thu nhỏ: mỗi chiều còn một nửa bằng Pillow BOX.

Seed và lựa chọn biến thể cho từng ảnh có trong manifest. Đây là dữ liệu đầu
vào được biến đổi có kiểm soát, không phải hình kết quả tạo tranh. Chỉ sáu
ảnh nền độc lập nên kết luận thực nghiệm cần giữ trong phạm vi tập nhỏ này.
