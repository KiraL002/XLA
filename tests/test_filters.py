"""Kiểm thử bộ lọc trung bình."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

from processing.filters import mean_filter


class MeanFilterTests(unittest.TestCase):
    def test_constant_image_is_unchanged_for_both_kernel_sizes(self) -> None:
        gray = np.full((5, 5), 80.0, dtype=np.float32)

        for ksize in (3, 5):
            with self.subTest(ksize=ksize):
                result = mean_filter(gray, ksize=ksize)
                np.testing.assert_array_equal(result, gray)

    def test_impulse_matches_hand_calculation(self) -> None:
        path = Path(__file__).parents[1] / "data" / "test_matrices" / "impulse_5x5.csv"
        gray = np.loadtxt(path, delimiter=",", dtype=np.float32)
        expected = np.zeros((5, 5), dtype=np.float32)
        expected[1:4, 1:4] = np.float32(255.0 / 9.0)

        np.testing.assert_allclose(mean_filter(gray, ksize=3), expected, atol=1e-6)

    def test_constant_matrix_csv(self) -> None:
        path = Path(__file__).parents[1] / "data" / "test_matrices" / "constant_5x5.csv"
        gray = np.loadtxt(path, delimiter=",", dtype=np.float32)

        np.testing.assert_array_equal(mean_filter(gray, ksize=3), gray)

    def test_edge_pixels_are_replicated(self) -> None:
        gray = np.array([[0.0, 90.0], [180.0, 255.0]], dtype=np.float32)
        padded = np.pad(gray, ((1, 1), (1, 1)), mode="edge")
        expected = np.empty_like(gray)

        for row in range(gray.shape[0]):
            for col in range(gray.shape[1]):
                expected[row, col] = padded[row : row + 3, col : col + 3].mean()

        np.testing.assert_allclose(mean_filter(gray, ksize=3), expected, atol=1e-6)

    def test_kernel_5_on_image_smaller_than_kernel_keeps_shape(self) -> None:
        gray = np.array([[0.0, 100.0]], dtype=np.float32)

        result = mean_filter(gray, ksize=5)

        self.assertEqual(result.shape, gray.shape)
        self.assertEqual(result.dtype, np.float32)
        self.assertTrue(np.isfinite(result).all())

    def test_input_is_not_modified(self) -> None:
        gray = np.arange(20, dtype=np.float32).reshape(4, 5)
        original = gray.copy()

        mean_filter(gray, ksize=3)

        np.testing.assert_array_equal(gray, original)

    def test_invalid_kernel_size_raises_value_error(self) -> None:
        gray = np.ones((3, 3), dtype=np.float32)

        for ksize in (1, 2, 4, 7, 3.0, True):
            with self.subTest(ksize=ksize):
                with self.assertRaises(ValueError):
                    mean_filter(gray, ksize=ksize)  # type: ignore[arg-type]

    def test_invalid_image_inputs_raise_value_error(self) -> None:
        invalid_inputs = (
            np.ones((3, 3), dtype=np.float64),
            np.ones((3, 3, 1), dtype=np.float32),
            np.empty((0, 3), dtype=np.float32),
            np.array([[np.nan]], dtype=np.float32),
            np.array([[np.inf]], dtype=np.float32),
            np.array([[-1.0]], dtype=np.float32),
            np.array([[256.0]], dtype=np.float32),
        )

        for gray in invalid_inputs:
            with self.subTest(shape=gray.shape, dtype=gray.dtype):
                with self.assertRaises(ValueError):
                    mean_filter(gray)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            mean_filter([[1.0, 2.0]])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
