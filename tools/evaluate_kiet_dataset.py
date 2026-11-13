"""Chạy phần mức xám trên manifest thật và lập kế hoạch chờ tích hợp."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import platform
from statistics import median
from time import perf_counter

import cv2
import numpy as np
from PIL import Image, ImageDraw, __version__ as pillow_version

from evaluation.reference import reference_grayscale
from image_io import load_rgb
from processing.grayscale import to_grayscale

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def runtime_ms(function):
    function()
    samples = []
    for _ in range(5):
        start = perf_counter(); function(); samples.append((perf_counter() - start) * 1000)
    return median(samples)


def main() -> int:
    image_dir = ROOT / 'data/test_images'
    output = ROOT / 'results/kiet_preparation'
    output.mkdir(parents=True, exist_ok=True)
    with (image_dir / 'manifest.csv').open(encoding='utf-8-sig', newline='') as handle:
        manifest = list(csv.DictReader(handle))
    if not manifest:
        raise ValueError('Manifest chưa có ảnh.')
    rows = []
    collage = Image.new('RGB', (1000, 6 * 200), 'white')
    draw = ImageDraw.Draw(collage)
    for index, entry in enumerate(manifest):
        source = image_dir / entry['filename']
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f"Tệp không khớp manifest: {source.name}")
        rgb = load_rgb(source)
        original = rgb.copy()
        gray = to_grayscale(rgb)
        reference = reference_grayscale(rgb)
        difference = np.abs(gray.astype(np.float64) - reference.astype(np.float64))
        valid = (gray.shape == rgb.shape[:2] and gray.dtype == np.float32
                 and np.isfinite(gray).all() and gray.min() >= 0 and gray.max() <= 255
                 and np.array_equal(original, rgb) and difference.max() <= 5e-5)
        row = dict(image_id=entry['image_id'], filename=entry['filename'], split=entry['split'],
                   base_id=entry['base_id'], condition=entry['condition'],
                   width=rgb.shape[1], height=rgb.shape[0], gray_min=float(gray.min()),
                   gray_max=float(gray.max()), gray_mean=float(gray.mean(dtype=np.float64)),
                   mae=float(difference.mean()), max_error=float(difference.max()),
                   numpy_ms=runtime_ms(lambda: to_grayscale(rgb)),
                   opencv_ms=runtime_ms(lambda: reference_grayscale(rgb)), status='Đạt' if valid else 'Lỗi')
        rows.append(row)
        target = output / entry['image_id']; target.mkdir(exist_ok=True)
        np.save(target / 'gray_float32.npy', gray)
        preview = Image.fromarray(np.rint(gray).astype(np.uint8))
        preview.save(target / 'gray_preview.png')
        thumb = preview.convert('RGB'); thumb.thumbnail((310, 155))
        x, y = (index % 3) * 333, (index // 3) * 200
        collage.paste(thumb, (x + (333 - thumb.width) // 2, y + 30))
        draw.text((x + 6, y + 5), f"{entry['image_id']} {entry['base_id']} / {entry['condition']}", fill='black')
    write_csv(output / 'grayscale_results.csv', rows)
    collage.save(output / 'grayscale_contact_sheet.jpg', quality=90)
    summary = dict(date='2026-11-06', scope='Mức xám trên ảnh chụp công khai và biến thể kiểm soát; chưa chạy tranh toàn luồng',
                   images=len(rows), independent_sources=len({r['base_id'] for r in rows}),
                   passed=sum(r['status'] == 'Đạt' for r in rows),
                   max_error=max(r['max_error'] for r in rows), mean_image_mae=float(np.mean([r['mae'] for r in rows])),
                   python=platform.python_version(), numpy=np.__version__, Pillow=pillow_version,
                   opencv=cv2.__version__, timing='Trung vị 5 lần sau 1 lần làm nóng; chỉ chuyển xám, không đọc/lưu tệp',
                   observations=rows)
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    report = [
        '# Thực nghiệm mức xám trên bộ ảnh có nguồn', '', 'Ngày thực chạy: 06 tháng 11 năm 2026.', '',
        f"Đã xử lý {len(rows)} ảnh: 6 ảnh chụp gốc công khai và 12 biến thể kiểm soát, không phải 18 cảnh độc lập.",
        'Chạy phần mức xám trên cả hai nhóm chỉ kiểm tra cài đặt; chưa dùng nhóm evaluation để chọn k hoặc T.', '',
        f"Kết quả: {summary['passed']}/{len(rows)} ảnh đạt tiêu chí kiểu, dạng, miền giá trị, không sửa đầu vào và sai số đối chiếu.",
        f"Sai số lớn nhất so OpenCV: {summary['max_error']:.10g}; trung bình MAE của 18 ảnh: {summary['mean_image_mae']:.10g}.",
        'Ngưỡng kiểm tra số thực: sai số lớn nhất không vượt 5e-5. MAE đánh giá độ khớp cài đặt, không đánh giá thẩm mỹ.', '',
        '| Ảnh | Nhóm | Biến thể | Kích thước | Mức xám trung bình | MAE | Lỗi lớn nhất | Trạng thái |',
        '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in rows:
        report.append(f"| {r['image_id']} {r['base_id']} | {r['split']} | {r['condition']} | {r['width']}×{r['height']} | {r['gray_mean']:.3f} | {r['mae']:.7g} | {r['max_error']:.7g} | {r['status']} |")
    report += ['', '## Cách chạy lại', '', '```powershell', 'cd D:\\XLA\\tranh_ve',
               '.\\.venv\\Scripts\\python.exe -m tools.evaluate_kiet_dataset', '```', '',
               'Thời gian trong CSV là trung vị 5 lần sau làm nóng, chỉ tính chuyển mức xám. Khi chạy lại số thời gian có thể đổi.',
               'Nguồn và phép biến đổi: `data/test_images/manifest.csv`; ảnh tải về được kiểm SHA256 với registry scikit-image v0.25.2.',
               'Ảnh xem trước, mảng float32, bảng CSV và JSON: `results/kiet_preparation/`.', '',
               '## Giới hạn', '', 'Chưa chạy bộ lọc, Sobel, pipeline hoặc giao diện. Các dự đoán ảnh khó là giả thuyết kiểm thử, chưa là kết quả tranh.',
               'Tập ảnh nhỏ và có ảnh chuẩn công khai; chưa chứng minh khả năng tổng quát. Có thể bổ sung ảnh nhóm tự chụp sau.']
    (ROOT / 'docs/KIET_THUC_NGHIEM_ANH_THAT.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    # Kế hoạch không điền số liệu chưa đo. Không ghi đè khi nhóm đã bắt đầu điền.
    plan = []
    for entry in manifest:
        pairs = [(k, t) for k in (3, 5) for t in (50, 100, 150)] if entry['split'] == 'tuning' else [('', '')]
        for k, threshold in pairs:
            plan.append(dict(case_id=f"P{len(plan)+1:03d}", image_id=entry['image_id'], split=entry['split'],
                             k= k, threshold=threshold, expected='Tranh cùng H×W, uint8, chỉ 0/255; nhận xét nét thừa/mất',
                             actual='', runtime_ms='', mae_reference='', different_pixel_rate='',
                             status='Chưa chạy', notes='Chờ bộ lọc/Sobel/pipeline' if k != '' else 'Chốt k/T từ tuning trước khi chạy evaluation'))
    plan_path = ROOT / 'docs/KE_HOACH_KIEM_THU_TICH_HOP.csv'
    if not plan_path.exists():
        write_csv(plan_path, plan)
    snapshot = dict(manifest=manifest, grayscale=rows, integration_plan=plan)
    (output / 'workbook_inputs.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key:value for key,value in summary.items() if key != 'observations'}, ensure_ascii=False, indent=2))
    return 0 if summary['passed'] == len(rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
