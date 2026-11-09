"""Kiểm thử bộ điều phối (Long). Chạy: python -m unittest tests.test_pipeline -v

"""

import unittest
from unittest import mock

import numpy as np

import pipeline
from pipeline import RESULT_KEYS, magnitude_preview, run_pipeline, validate_params


def fake_rgb(h=6, w=8):
    return np.random.default_rng(1).integers(0, 256, (h, w, 3), dtype=np.uint8)


class TestValidation(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_params(3, 100), (3, 100.0))
        self.assertEqual(validate_params(5, 0.0), (5, 0.0))

    def test_invalid_ksize(self):
        for k in (0, 1, 2, 4, 7, -3, 3.0, "3", None, True):
            with self.subTest(k=k), self.assertRaises(ValueError):
                validate_params(k, 100.0)

    def test_invalid_threshold(self):
        for t in (-1, -0.01, float("nan"), float("inf"), "100", None, True):
            with self.subTest(t=t), self.assertRaises(ValueError):
                validate_params(3, t)

    def test_invalid_image(self):
        for bad in (np.zeros((4, 4), np.uint8), np.zeros((4, 4, 4), np.uint8),
                    np.zeros((4, 4, 3), np.float32), np.zeros((0, 4, 3), np.uint8), "x"):
            with self.subTest(shape=getattr(bad, "shape", None)), self.assertRaises(ValueError):
                run_pipeline(bad)


class TestWiringWithMocks(unittest.TestCase):
    def setUp(self):
        h, w = 6, 8
        self.gray = np.full((h, w), 10, np.float32)
        self.smooth = np.full((h, w), 20, np.float32)
        self.mag = np.full((h, w), 300.0, np.float32)  # thô, > 255
        self.edges = np.ones((h, w), bool)
        self.sketch = np.zeros((h, w), np.uint8)
        self.patches = {
            "to_grayscale": mock.Mock(return_value=self.gray),
            "mean_filter": mock.Mock(return_value=self.smooth),
            "sobel_magnitude": mock.Mock(return_value=self.mag),
            "threshold_edges": mock.Mock(return_value=self.edges),
            "render_sketch": mock.Mock(return_value=self.sketch),
        }
        self._ctx = [mock.patch.object(pipeline, n, m) for n, m in self.patches.items()]
        for c in self._ctx:
            c.start()
        self.addCleanup(lambda: [c.stop() for c in self._ctx])

    def test_keys_and_order(self):
        rgb = fake_rgb()
        out = run_pipeline(rgb, 5, 42.0)
        self.assertEqual(tuple(out.keys()), RESULT_KEYS)
        self.patches["to_grayscale"].assert_called_once_with(rgb)
        self.patches["mean_filter"].assert_called_once_with(self.gray, 5)
        self.patches["sobel_magnitude"].assert_called_once_with(self.smooth)
        self.patches["threshold_edges"].assert_called_once_with(self.mag, 42.0)
        self.patches["render_sketch"].assert_called_once_with(self.edges)

    def test_threshold_receives_raw_magnitude(self):
        run_pipeline(fake_rgb())
        passed = self.patches["threshold_edges"].call_args[0][0]
        self.assertIs(passed, self.mag)
        self.assertGreater(float(passed.max()), 255.0)

    def test_invalid_params_do_not_run_steps(self):
        with self.assertRaises(ValueError):
            run_pipeline(fake_rgb(), 4, 100.0)
        self.patches["to_grayscale"].assert_not_called()

    def test_input_not_modified(self):
        rgb = fake_rgb()
        before = rgb.copy()
        run_pipeline(rgb)
        np.testing.assert_array_equal(rgb, before)


class TestPreview(unittest.TestCase):
    def test_preview_scales_to_uint8_and_keeps_input(self):
        m = np.array([[0.0, 150.0], [300.0, 75.0]], np.float32)
        before = m.copy()
        p = magnitude_preview(m)
        self.assertEqual(p.dtype, np.uint8)
        self.assertEqual(int(p.max()), 255)
        np.testing.assert_array_equal(m, before)

    def test_preview_all_zero(self):
        self.assertTrue(np.all(magnitude_preview(np.zeros((3, 3), np.float32)) == 0))


class TestRealModules(unittest.TestCase):
    """Chạy hàm thật của cả nhóm; bỏ qua nếu bước nào chưa triển khai."""

    def _run(self, rgb, k=3, t=100.0):
        try:
            return run_pipeline(rgb, k, t)
        except NotImplementedError as exc:
            self.skipTest(f"Chưa triển khai: {exc}")

    def test_full_flow_contract(self):
        rgb = np.zeros((16, 16, 3), np.uint8)
        rgb[:, 8:] = 255
        for k in (3, 5):
            out = self._run(rgb, k, 100.0)
            self.assertEqual(tuple(out), RESULT_KEYS)
            for key in RESULT_KEYS:
                self.assertEqual(out[key].shape, (16, 16))
            self.assertEqual(out["gray"].dtype, np.float32)
            self.assertEqual(out["smooth"].dtype, np.float32)
            self.assertEqual(out["magnitude"].dtype, np.float32)
            self.assertEqual(out["edges"].dtype, np.bool_)
            self.assertEqual(out["sketch"].dtype, np.uint8)
            self.assertTrue(set(np.unique(out["sketch"])) <= {0, 255})
            self.assertTrue(np.any(out["edges"]))  # có cạnh dọc rõ ràng

    def test_constant_image_has_no_edges(self):
        out = self._run(np.full((10, 10, 3), 80, np.uint8))
        self.assertFalse(np.any(out["edges"]))
        self.assertTrue(np.all(out["sketch"] == 255))

    def test_higher_threshold_not_more_edges(self):
        rng = np.random.default_rng(3)
        rgb = rng.integers(0, 256, (24, 24, 3), dtype=np.uint8)
        low = self._run(rgb, 3, 50.0)["edges"].sum()
        high = self._run(rgb, 3, 200.0)["edges"].sum()
        self.assertGreaterEqual(int(low), int(high))


if __name__ == "__main__":
    unittest.main()