"""Tạo hình minh họa và bảng đối chiếu tranh từ bộ ảnh của nhóm."""

from __future__ import annotations

import csv
from itertools import product
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from evaluation.reference import run_reference_pipeline
from image_io import load_rgb
from pipeline import ALLOWED_KSIZES, magnitude_preview, run_pipeline

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "data/test_images"
OUTPUT_DIR = ROOT / "results/sketch_evaluation"
EXAMPLES = {
    "I04": "Cốc cà phê",
    "I02": "Phi hành gia bản tối",
    "I11": "Mèo có nhiễu muối tiêu",
}


def save_figure(path, title, caption, panels, columns):
    """Đặt ảnh cùng tỷ lệ trong các ô có nhãn, dùng cho báo cáo và slide."""
    tile_width, tile_height = 320, 250
    margin, header_height = 24, 92
    rows = (len(panels) + columns - 1) // columns
    figure = Image.new(
        "RGB",
        (2 * margin + columns * tile_width, header_height + rows * tile_height + margin),
        "white",
    )
    draw = ImageDraw.Draw(figure)
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 30)
        label_font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        title_font = ImageFont.load_default(size=30)
        label_font = ImageFont.load_default(size=22)
    draw.text((margin, 15), title, fill="#17212b", font=title_font)
    draw.text((margin, 54), caption, fill="#354758", font=label_font)
    for index, (label, array) in enumerate(panels):
        row, column = divmod(index, columns)
        x = margin + column * tile_width
        y = header_height + row * tile_height
        image = Image.fromarray(array)
        image.thumbnail((tile_width - 16, tile_height - 38), Image.Resampling.LANCZOS)
        draw.text((x + tile_width / 2, y), label, anchor="mt", fill="#17212b", font=label_font)
        left = x + (tile_width - image.width) // 2
        top = y + 30 + (tile_height - 38 - image.height) // 2
        figure.paste(image, (left, top))
        draw.rectangle((left - 1, top - 1, left + image.width, top + image.height), outline="#ccd4dc")
    figure.save(path)


def main() -> None:
    with (IMAGE_DIR / "manifest.csv").open(encoding="utf-8-sig", newline="") as source:
        entries = list(csv.DictReader(source))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    comparisons = []
    examples = {}

    for entry in entries:
        image_id = entry["image_id"]
        rgb = load_rgb(IMAGE_DIR / entry["filename"])
        for ksize, threshold in product(ALLOWED_KSIZES, (50, 100, 150)):
            result = run_pipeline(rgb, ksize, threshold)
            reference = run_reference_pipeline(rgb, ksize, threshold)
            difference = np.abs(result["magnitude"] - reference["magnitude"])
            different_pixels = int(np.count_nonzero(result["sketch"] != reference["sketch"]))
            comparisons.append({
                "image_id": image_id,
                "filename": entry["filename"],
                "ksize": ksize,
                "threshold": threshold,
                "gradient_mae": float(difference.mean(dtype=np.float64)),
                "gradient_max_error": float(difference.max()),
                "different_pixels": different_pixels,
                "different_pixel_percent": 100 * different_pixels / difference.size,
            })
            if image_id in EXAMPLES and (ksize, threshold) == (3, 100):
                thinned = run_pipeline(rgb, ksize, threshold, thin=True)["sketch"]
                pencil = run_pipeline(rgb, ksize, threshold, mode="pencil")["sketch"]
                examples[image_id] = (rgb, result, reference["sketch"], thinned, pencil)

    with (OUTPUT_DIR / "doi_chieu_opencv.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)

    rgb, result, reference, _, _ = examples["I04"]
    save_figure(
        OUTPUT_DIR / "cac_buoc_xu_ly.png",
        "Các bước chuyển ảnh thành tranh nét",
        "I04 · Cốc cà phê · Cửa sổ 3×3 · Ngưỡng 100",
        [
            ("Ảnh gốc", rgb),
            ("Mức xám", np.clip(result["gray"], 0, 255).astype(np.uint8)),
            ("Làm mịn", np.clip(result["smooth"], 0, 255).astype(np.uint8)),
            ("Gradient (xem trước)", magnitude_preview(result["magnitude"])),
            ("Tranh tự cài đặt", result["sketch"]),
            ("Tham chiếu OpenCV", reference),
        ],
        columns=3,
    )

    panels = []
    pencil_panels = []
    for image_id, name in EXAMPLES.items():
        rgb, result, _, thinned, pencil = examples[image_id]
        before = np.count_nonzero(result["sketch"] == 0)
        after = np.count_nonzero(thinned == 0)
        panels.extend([
            (f"{image_id} · {name}", rgb),
            (f"Tranh nét · {before:,} điểm", result["sketch"]),
            (f"Làm mảnh · {after:,} điểm", thinned),
        ])
        pencil_panels.extend([
            (f"{image_id} · {name}", rgb),
            ("Tranh nét", result["sketch"]),
            ("Tranh chì có sắc độ", pencil),
        ])
    save_figure(
        OUTPUT_DIR / "so_sanh_lam_manh.png",
        "So sánh tranh trước và sau làm mảnh",
        "Zhang–Suen · Cửa sổ 3×3 · Ngưỡng 100 trên cả ba ảnh",
        panels,
        columns=3,
    )
    save_figure(
        OUTPUT_DIR / "so_sanh_tranh_chi.png",
        "Tranh nét và tranh chì có sắc độ",
        "Cửa sổ 3×3 · Ngưỡng 100 · Lọc trung vị 3×3 trong chế độ tranh chì",
        pencil_panels,
        columns=3,
    )

    identical = sum(row["different_pixels"] == 0 for row in comparisons)
    print(f"Pixel-identical comparisons: {identical}/{len(comparisons)}")
    print(f"Figures and CSV: {OUTPUT_DIR.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
