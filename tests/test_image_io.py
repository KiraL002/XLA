"""Kiểm tra đọc ảnh thật từ tệp tạm và lưu PNG không mất giá trị."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from image_io import load_rgb, save_sketch


class ImageIOTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def test_read_rgb_png_and_unicode_path(self):
        rgb = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [10, 20, 30]]], np.uint8)
        path = self.root / 'ảnh có dấu.png'
        Image.fromarray(rgb).save(path)
        result = load_rgb(path)
        np.testing.assert_array_equal(result, rgb)
        self.assertEqual(result.dtype, np.uint8)
        self.assertTrue(result.flags.writeable)
        path.unlink()  # Tệp đã đóng sau khi đọc.
        np.testing.assert_array_equal(result, rgb)

    def test_read_grayscale_png(self):
        gray = np.array([[0, 80], [127, 255]], np.uint8)
        path = self.root / 'gray.png'
        Image.fromarray(gray).save(path)
        result = load_rgb(str(path))
        self.assertEqual(result.shape, (2, 2, 3))
        for channel in range(3):
            np.testing.assert_array_equal(result[:, :, channel], gray)

    def test_read_jpeg(self):
        path = self.root / 'red.jpg'
        Image.new('RGB', (8, 6), (240, 10, 10)).save(path, quality=95)
        result = load_rgb(path)
        self.assertEqual(result.shape, (6, 8, 3))
        self.assertTrue((result[:, :, 0] > 200).all())
        self.assertTrue((result[:, :, 2] < 30).all())

    def test_transparent_rgba_uses_white_background(self):
        path = self.root / 'alpha.png'
        rgba = np.array([[[255, 0, 0, 0], [0, 0, 255, 255]]], np.uint8)
        Image.fromarray(rgba).save(path)
        np.testing.assert_array_equal(load_rgb(path), [[[255, 255, 255], [0, 0, 255]]])

    def test_palette_transparency(self):
        path = self.root / 'palette.png'
        image = Image.new('P', (2, 1))
        image.putpalette([0, 0, 0, 255, 0, 0] + [0] * 762)
        image.putdata([0, 1])
        image.save(path, transparency=0)
        np.testing.assert_array_equal(load_rgb(path), [[[255, 255, 255], [255, 0, 0]]])

    def test_exif_orientation_is_applied(self):
        rgb = np.arange(18, dtype=np.uint8).reshape(2, 3, 3)
        image = Image.fromarray(rgb)
        exif = image.getexif()
        exif[274] = 6  # Xoay 90 độ theo chiều kim đồng hồ khi hiển thị.
        path = self.root / 'oriented.png'
        image.save(path, exif=exif)
        np.testing.assert_array_equal(load_rgb(path), np.rot90(rgb, k=-1))

    def test_missing_corrupt_and_unsupported_files(self):
        with self.assertRaises(FileNotFoundError):
            load_rgb(self.root / 'missing.png')
        bad = self.root / 'bad.png'
        bad.write_bytes(b'not an image')
        with self.assertRaises(OSError):
            load_rgb(bad)
        bmp = self.root / 'not_supported.bmp'
        Image.new('RGB', (2, 2)).save(bmp)
        with self.assertRaises(ValueError):
            load_rgb(bmp)

    def test_invalid_paths(self):
        for value in [None, 1, '', b'image.png', 'nul\x00.png']:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    load_rgb(value)

    def test_save_and_read_png_exactly(self):
        sketch = np.array([[0, 255, 0], [255, 255, 0]], np.uint8)
        original = sketch.copy()
        path = self.root / 'tranh kết quả.PNG'
        self.assertIsNone(save_sketch(path, sketch))
        with Image.open(path) as result:
            self.assertEqual(result.format, 'PNG')
            self.assertEqual(result.mode, 'L')
            np.testing.assert_array_equal(np.array(result), sketch)
        np.testing.assert_array_equal(sketch, original)

    def test_invalid_sketch_does_not_overwrite_existing_file(self):
        target = self.root / 'existing.png'
        target.write_bytes(b'keep existing contents')
        cases = [None, [[0]], np.zeros((1, 2), np.float32),
                 np.zeros((0, 2), np.uint8), np.zeros((2,), np.uint8),
                 np.zeros((2, 2, 3), np.uint8), np.array([[127]], np.uint8)]
        for value in cases:
            with self.subTest(shape=getattr(value, 'shape', None)):
                with self.assertRaises(ValueError):
                    save_sketch(target, value)
                self.assertEqual(target.read_bytes(), b'keep existing contents')

    def test_save_preserves_pencil_tones(self):
        pencil = np.array([[0, 65, 127, 220, 255]], dtype=np.uint8)
        path = self.root / 'pencil.png'
        save_sketch(path, pencil, allow_gray=True)

        with Image.open(path) as result:
            self.assertEqual(result.mode, 'L')
            np.testing.assert_array_equal(np.asarray(result), pencil)

    def test_save_rejects_wrong_extension(self):
        with self.assertRaises(ValueError):
            save_sketch(self.root / 'wrong.jpg', np.zeros((1, 1), np.uint8))
        self.assertFalse((self.root / 'wrong.jpg').exists())

    def test_write_failure_preserves_existing_file_and_removes_temporary_file(self):
        target = self.root / 'existing.png'
        target.write_bytes(b'original contents')

        def fail_after_partial_write(image, path, *args, **kwargs):
            Path(path).write_bytes(b'partial contents')
            raise OSError('simulated disk error')

        with patch.object(Image.Image, 'save', new=fail_after_partial_write):
            with self.assertRaises(OSError):
                save_sketch(target, np.zeros((2, 2), np.uint8))
        self.assertEqual(target.read_bytes(), b'original contents')
        self.assertEqual(list(self.root.iterdir()), [target])

    def test_missing_output_directory_is_reported(self):
        with self.assertRaises(OSError):
            save_sketch(self.root / 'missing' / 'out.png', np.zeros((1, 1), np.uint8))


if __name__ == '__main__':
    unittest.main()
