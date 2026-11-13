"""Tải ảnh mẫu có nguồn, tạo 18 ca thử có biến thể và chia nhóm theo ảnh gốc."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/scikit-image/scikit-image/v0.25.2/skimage/data/'
DOC = 'https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.'
SOURCES = [
    ('astronaut', 'astronaut.png', 'tuning', 'NASA', 'Public domain', 'Chân dung, nền có chi tiết', ['original', 'dark', 'gaussian_noise']),
    ('coffee', 'coffee.png', 'tuning', 'Rachel Michetti', 'CC0', 'Cốc cà phê, đường cong và vân gỗ', ['original', 'bright', 'half_size']),
    ('grass', 'grass.png', 'tuning', 'Nguồn DeviantArt qua scikit-image; xem tài liệu nguồn', 'CC0', 'Cỏ, ảnh xám có nhiều kết cấu', ['original', 'salt_pepper', 'half_size']),
    ('chelsea', 'chelsea.png', 'evaluation', 'Stefan van der Walt', 'CC0', 'Mèo, lông và đường nét nhỏ', ['original', 'salt_pepper', 'dark']),
    ('camera', 'camera.png', 'evaluation', 'Lav Varshney', 'CC0', 'Người và máy ảnh, ảnh xám', ['original', 'bright', 'half_size']),
    ('rocket', 'rocket.jpg', 'evaluation', 'SpaceX', 'Public domain theo scikit-image', 'Tên lửa ngoài trời, vùng sáng và nền tối', ['original', 'dark', 'gaussian_noise']),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url: str) -> bytes:
    request = Request(url, headers={'User-Agent': 'PTIT-XLA-educational-test-data/1.0'})
    with urlopen(request, timeout=40) as response:
        return response.read()


def transform(pixels: np.ndarray, condition: str, seed: int):
    rng = np.random.default_rng(seed)
    if condition == 'original':
        return pixels.copy(), 'Không biến đổi; giải mã và lưu PNG'
    if condition == 'dark':
        return np.rint(pixels.astype(np.float32) * 0.35).astype(np.uint8), 'round(0.35 * I)'
    if condition == 'bright':
        return np.rint(np.clip(pixels.astype(np.float32) * 1.7 + 20, 0, 255)).astype(np.uint8), 'round(clip(1.7 * I + 20, 0, 255))'
    if condition == 'half_size':
        h, w = pixels.shape[:2]
        result = Image.fromarray(pixels).resize((max(1, w // 2), max(1, h // 2)), Image.Resampling.BOX)
        return np.array(result), 'Resize còn một nửa mỗi chiều, Pillow BOX'
    if condition == 'gaussian_noise':
        noise = rng.normal(0, 20, pixels.shape)
        return np.rint(np.clip(pixels.astype(np.float64) + noise, 0, 255)).astype(np.uint8), 'I + N(0,20^2), clip 0..255, nhiễu độc lập từng kênh'
    if condition == 'salt_pepper':
        result = pixels.copy()
        mask = rng.random(pixels.shape[:2])
        result[mask < 0.015] = 0
        result[(mask >= 0.015) & (mask < 0.03)] = 255
        return result, 'Xác suất tiêu 1.5%, muối 1.5%, cùng vị trí trên các kênh'
    raise ValueError(f'Biến thể không hỗ trợ: {condition}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', help='Tải sáu ảnh gốc và registry SHA256')
    args = parser.parse_args()
    source_dir = ROOT / 'data/source_images'
    image_dir = ROOT / 'data/test_images'
    source_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)
    registry_path = source_dir / 'registry.json'
    if args.download:
        # Chỉ đọc literal của registry, không thực thi mã từ Internet.
        tree = ast.parse(fetch(RAW + '_registry.py').decode('utf-8'))
        registry = next(ast.literal_eval(n.value) for n in tree.body
                        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'registry' for t in n.targets))
        expected = {file: registry['data/' + file] for _, file, *_ in SOURCES}
        for _, file, *_ in SOURCES:
            path = source_dir / file
            content = fetch(RAW + file)
            if hashlib.sha256(content).hexdigest() != expected[file]:
                raise ValueError(f'SHA256 không khớp registry: {file}')
            path.write_bytes(content)
            print(f'Đã tải và kiểm tra SHA256: {file}', flush=True)
        registry_path.write_text(json.dumps(expected, indent=2), encoding='utf-8')
    expected = json.loads(registry_path.read_text(encoding='utf-8'))
    rows, credits = [], []
    index = 0
    for base_index, (base, file, split, author, license_name, description, conditions) in enumerate(SOURCES):
        source = source_dir / file
        if sha256(source) != expected[file]:
            raise ValueError(f'Ảnh gốc thay đổi: {file}')
        with Image.open(source) as image:
            pixels = np.array(image)
        credits.append(dict(base_id=base, filename=file, author=author, license=license_name,
                            documentation=DOC + base, download_url=RAW + file, sha256=expected[file],
                            registry_url=RAW + '_registry.py', retrieved_date='2026-11-06'))
        for condition in conditions:
            index += 1
            image_id = f'I{index:02d}'
            seed = 20261106 + base_index
            changed, recipe = transform(pixels, condition, seed)
            filename = f'{image_id}_{base}_{condition}.png'
            path = image_dir / filename
            Image.fromarray(changed).save(path)
            rows.append(dict(image_id=image_id, filename=filename, source=DOC + base,
                             description=description, split=split, base_id=base, condition=condition,
                             transform=recipe, width=changed.shape[1], height=changed.shape[0],
                             mode='RGB' if changed.ndim == 3 else 'L', author=author,
                             license=license_name, source_file_url=RAW + file,
                             source_sha256=expected[file], sha256=sha256(path),
                             seed=seed if condition in {'gaussian_noise', 'salt_pepper'} else ''))
    # Chia nhóm theo ảnh gốc, không chia các biến thể sang nhóm khác.
    assert len(rows) == 18 and len({r['base_id'] for r in rows}) == 6
    for base, *_ in SOURCES:
        assert len({r['split'] for r in rows if r['base_id'] == base}) == 1
    with (image_dir / 'manifest.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    (source_dir / 'sources.json').write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding='utf-8')
    sheet = Image.new('RGB', (1050, 6 * 215), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x, y = (i % 3) * 350, (i // 3) * 215
        with Image.open(image_dir / row['filename']) as image:
            thumb = image.convert('RGB'); thumb.thumbnail((330, 170))
            sheet.paste(thumb, (x + (350 - thumb.width) // 2, y + 30))
        draw.text((x + 10, y + 5), f"{row['image_id']} {row['base_id']} / {row['condition']} / {row['split']}", fill='black')
    output = ROOT / 'results/dataset'
    output.mkdir(parents=True, exist_ok=True)
    sheet.save(output / 'dataset_contact_sheet.jpg', quality=90)
    print('Đã chuẩn bị 18 ảnh: 9 tuning, 9 evaluation; 6 ảnh gốc độc lập.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
