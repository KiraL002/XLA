# Thực nghiệm mức xám trên bộ ảnh có nguồn

Ngày thực chạy: 06 tháng 11 năm 2026.

Đã xử lý 18 ảnh: 6 ảnh chụp gốc công khai và 12 biến thể kiểm soát, không phải 18 cảnh độc lập.
Chạy phần mức xám trên cả hai nhóm chỉ kiểm tra cài đặt; chưa dùng nhóm evaluation để chọn k hoặc T.

Kết quả: 18/18 ảnh đạt tiêu chí kiểu, dạng, miền giá trị, không sửa đầu vào và sai số đối chiếu.
Sai số lớn nhất so OpenCV: 3.051757812e-05; trung bình MAE của 18 ảnh: 1.434982315e-06.
Ngưỡng kiểm tra số thực: sai số lớn nhất không vượt 5e-5. MAE đánh giá độ khớp cài đặt, không đánh giá thẩm mỹ.

| Ảnh | Nhóm | Biến thể | Kích thước | Mức xám trung bình | MAE | Lỗi lớn nhất | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I01 astronaut | tuning | original | 512×512 | 115.406 | 2.034569e-06 | 3.051758e-05 | Đạt |
| I02 astronaut | tuning | dark | 512×512 | 40.390 | 7.468018e-07 | 1.525879e-05 | Đạt |
| I03 astronaut | tuning | gaussian_noise | 512×512 | 116.701 | 2.050393e-06 | 3.051758e-05 | Đạt |
| I04 coffee | tuning | original | 600×400 | 103.643 | 2.01115e-06 | 3.051758e-05 | Đạt |
| I05 coffee | tuning | bright | 600×400 | 167.458 | 1.997558e-06 | 3.051758e-05 | Đạt |
| I06 coffee | tuning | half_size | 300×200 | 104.140 | 1.989118e-06 | 3.051758e-05 | Đạt |
| I07 grass | tuning | original | 512×512 | 118.224 | 1.399949e-06 | 1.525879e-05 | Đạt |
| I08 grass | tuning | salt_pepper | 512×512 | 118.535 | 1.357694e-06 | 1.525879e-05 | Đạt |
| I09 grass | tuning | half_size | 256×256 | 118.725 | 1.433873e-06 | 1.525879e-05 | Đạt |
| I10 chelsea | evaluation | original | 451×300 | 119.467 | 2.105886e-06 | 1.525879e-05 | Đạt |
| I11 chelsea | evaluation | salt_pepper | 451×300 | 119.670 | 2.040814e-06 | 1.525879e-05 | Đạt |
| I12 chelsea | evaluation | dark | 451×300 | 41.814 | 8.225846e-07 | 7.629395e-06 | Đạt |
| I13 camera | evaluation | original | 512×512 | 129.061 | 1.40008e-06 | 1.525879e-05 | Đạt |
| I14 camera | evaluation | bright | 512×512 | 194.287 | 5.293332e-07 | 1.525879e-05 | Đạt |
| I15 camera | evaluation | half_size | 256×256 | 129.530 | 1.427936e-06 | 1.525879e-05 | Đạt |
| I16 rocket | evaluation | original | 640×427 | 60.986 | 1.072903e-06 | 3.051758e-05 | Đạt |
| I17 rocket | evaluation | dark | 640×427 | 21.345 | 4.395644e-07 | 1.525879e-05 | Đạt |
| I18 rocket | evaluation | gaussian_noise | 640×427 | 61.274 | 9.694754e-07 | 3.051758e-05 | Đạt |

## Cách chạy lại

```powershell
cd D:\XLA\tranh_ve
.\.venv\Scripts\python.exe -m tools.evaluate_kiet_dataset
```

Thời gian trong CSV là trung vị 5 lần sau làm nóng, chỉ tính chuyển mức xám. Khi chạy lại số thời gian có thể đổi.
Nguồn và phép biến đổi: `data/test_images/manifest.csv`; ảnh tải về được kiểm SHA256 với registry scikit-image v0.25.2.
Ảnh xem trước, mảng float32, bảng CSV và JSON: `results/kiet_preparation/`.

## Giới hạn

Chưa chạy bộ lọc, Sobel, pipeline hoặc giao diện. Các dự đoán ảnh khó là giả thuyết kiểm thử, chưa là kết quả tranh.
Tập ảnh nhỏ và có ảnh chuẩn công khai; chưa chứng minh khả năng tổng quát. Có thể bổ sung ảnh nhóm tự chụp sau.
