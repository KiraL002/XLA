"""Demo độc lập phần Kiệt; chưa tính bộ lọc hoặc Sobel từ ảnh."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

from evaluation.reference import reference_grayscale
from image_io import load_rgb, save_sketch
from processing.grayscale import to_grayscale
from processing.sketch import render_sketch, threshold_edges


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, help='Ảnh JPG/PNG để chuyển mức xám')
    parser.add_argument('--magnitude', type=Path, help='CSV độ lớn gradient, không có tiêu đề')
    parser.add_argument('--threshold', type=float, default=100.0)
    parser.add_argument('--output-dir', type=Path, default=Path('results/kiet'))
    args = parser.parse_args()
    if args.image is None and args.magnitude is None:
        parser.error('Cần --image hoặc --magnitude; hai phần demo chạy độc lập.')
    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        report = {'scope': 'Demo độc lập phần Kiệt, chưa chạy toàn hệ thống.'}
        if args.image is not None:
            rgb = load_rgb(args.image)
            gray = to_grayscale(rgb)
            reference = reference_grayscale(rgb)
            # Chỉ ép uint8 ở bản xem trước; giữ float32 cho bước kế tiếp.
            Image.fromarray(np.rint(gray).astype(np.uint8)).save(args.output_dir / 'gray_preview.png')
            np.save(args.output_dir / 'gray_float32.npy', gray)
            error = np.abs(gray.astype(np.float64) - reference.astype(np.float64))
            report['grayscale'] = {
                'input': str(args.image.resolve()), 'shape': list(gray.shape),
                'mae_vs_opencv': float(error.mean()),
                'max_error_vs_opencv': float(error.max()),
            }
        if args.magnitude is not None:
            magnitude = np.loadtxt(args.magnitude, delimiter=',', dtype=np.float32, ndmin=2)
            edges = threshold_edges(magnitude, args.threshold)
            sketch = render_sketch(edges)
            save_sketch(args.output_dir / 'sketch_from_magnitude.png', sketch)
            report['sketch'] = {
                'magnitude_input': str(args.magnitude.resolve()),
                'threshold': args.threshold, 'shape': list(sketch.shape),
                'edge_pixels': int(edges.sum()),
                'note': 'Chỉ nhận ma trận đã cấp; demo không tính Sobel từ ảnh.',
            }
        text = json.dumps(report, ensure_ascii=False, indent=2)
        (args.output_dir / 'demo_report.json').write_text(text, encoding='utf-8')
        print(text)
    except (OSError, ValueError, ImportError) as exc:
        parser.exit(1, f'Không chạy được demo: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
