"""Kiểm tra mức xám bằng giá trị tính tay và OpenCV độc lập."""

import unittest

import numpy as np

from evaluation.reference import reference_grayscale
from processing.grayscale import to_grayscale


class GrayscaleTests(unittest.TestCase):
    def test_known_rgb_values_and_fractional_output(self):
        rgb = np.array([[
            [0, 0, 0], [255, 255, 255], [255, 0, 0],
            [0, 255, 0], [0, 0, 255], [10, 20, 30],
        ]], dtype=np.uint8)
        expected = [[0, 255, 76.245, 149.685, 29.07, 18.15]]
        result = to_grayscale(rgb)
        np.testing.assert_allclose(result, expected, rtol=0, atol=2e-5)
        self.assertEqual(result.dtype, np.float32)
        self.assertEqual(result.shape, (1, 6))

    def test_opencv_reference_on_reproducible_colors(self):
        rng = np.random.default_rng(2026)
        rgb = rng.integers(0, 256, (64, 97, 3), dtype=np.uint8)
        original = rgb.copy()
        result = to_grayscale(rgb)
        reference = reference_grayscale(rgb)
        self.assertEqual(reference.dtype, np.float32)
        np.testing.assert_allclose(result, reference, rtol=0, atol=5e-5)
        np.testing.assert_array_equal(rgb, original)

    def test_noncontiguous_readonly_input_and_independent_output(self):
        base = np.full((4, 6, 3), 80, dtype=np.uint8)
        rgb = base[::2, ::2]
        rgb.flags.writeable = False
        result = to_grayscale(rgb)
        np.testing.assert_allclose(result, 80, atol=1e-5)
        self.assertFalse(np.shares_memory(result, rgb))
        np.testing.assert_array_equal(base, 80)

    def test_invalid_inputs(self):
        cases = [None, [[[0, 0, 0]]], np.zeros((2, 3), np.uint8),
                 np.zeros((1, 1, 4), np.uint8), np.zeros((0, 2, 3), np.uint8),
                 np.zeros((1, 1, 3), np.float32), np.zeros((1, 1, 3), np.int16)]
        for value in cases:
            with self.subTest(shape=getattr(value, 'shape', None), type=type(value)):
                with self.assertRaises(ValueError):
                    to_grayscale(value)
                with self.assertRaises(ValueError):
                    reference_grayscale(value)


if __name__ == '__main__':
    unittest.main()
