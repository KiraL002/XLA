"""Kiểm tra quy tắc lấy biên và tạo tranh với dữ liệu tính tay."""

import unittest

import numpy as np

from processing.sketch import render_sketch, threshold_edges


class SketchTests(unittest.TestCase):
    def test_strict_threshold_and_magnitude_above_255(self):
        magnitude = np.array([[0, 99, 100, 101, 1000]], dtype=np.float32)
        original = magnitude.copy()
        edges = threshold_edges(magnitude)
        np.testing.assert_array_equal(edges, [[False, False, False, True, True]])
        self.assertEqual(edges.dtype, np.bool_)
        np.testing.assert_array_equal(magnitude, original)

    def test_zero_threshold_and_large_finite_threshold(self):
        magnitude = np.array([[0, 1, 2000]], np.float32)
        np.testing.assert_array_equal(threshold_edges(magnitude, 0), [[False, True, True]])
        np.testing.assert_array_equal(threshold_edges(magnitude, 1e100), [[False] * 3])

    def test_threshold_precision_near_a_float32_value(self):
        magnitude = np.array([[100]], np.float32)
        self.assertTrue(threshold_edges(magnitude, 99.999999)[0, 0])
        self.assertFalse(threshold_edges(magnitude, 100.000001)[0, 0])
        self.assertTrue(threshold_edges(magnitude, np.float32(99))[0, 0])

    def test_invalid_thresholds(self):
        magnitude = np.ones((1, 2), np.float32)
        for value in [-1, float('nan'), float('inf'), -float('inf'), True,
                      np.bool_(True), '100', None, 1+0j, [100], 10**1000]:
            with self.subTest(value_type=type(value)):
                with self.assertRaises(ValueError):
                    threshold_edges(magnitude, value)

    def test_invalid_magnitudes(self):
        cases = [None, [[1]], np.ones((1, 1), np.float64),
                 np.ones((2,), np.float32), np.zeros((2, 0), np.float32),
                 np.zeros((1, 1, 1), np.float32),
                 np.array([[-1]], np.float32), np.array([[np.nan]], np.float32),
                 np.array([[np.inf]], np.float32)]
        for value in cases:
            with self.subTest(shape=getattr(value, 'shape', None)):
                with self.assertRaises(ValueError):
                    threshold_edges(value)

    def test_black_edges_white_background_and_no_mutation(self):
        edges = np.array([[False, True, False], [True, False, True]])
        original = edges.copy()
        edges.flags.writeable = False
        sketch = render_sketch(edges)
        np.testing.assert_array_equal(sketch, [[255, 0, 255], [0, 255, 0]])
        self.assertEqual(sketch.dtype, np.uint8)
        self.assertFalse(np.shares_memory(sketch, edges))
        np.testing.assert_array_equal(edges, original)

    def test_uniform_masks(self):
        for flag, expected in [(False, 255), (True, 0)]:
            with self.subTest(flag=flag):
                np.testing.assert_array_equal(render_sketch(np.full((2, 3), flag)), expected)

    def test_invalid_masks(self):
        for value in [None, [[True]], np.ones((2, 2), np.uint8),
                      np.zeros((0, 2), bool), np.zeros((2,), bool),
                      np.zeros((1, 1, 1), bool)]:
            with self.subTest(shape=getattr(value, 'shape', None)):
                with self.assertRaises(ValueError):
                    render_sketch(value)


if __name__ == '__main__':
    unittest.main()
