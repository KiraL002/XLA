"""Kiểm thử toán tử Sobel.

Dữ liệu là mảng xác định trước/tự tạo, dùng kiểm tra số học,
không phải kết quả thực nghiệm trên ảnh thật.
"""

import unittest
from pathlib import Path

import numpy as np

from processing.edges import SOBEL_KX, SOBEL_KY, sobel_gradients, sobel_magnitude

try:
    import cv2
except ImportError:  # nhánh đối chiếu là tùy chọn
    cv2 = None


MATRICES = Path(__file__).resolve().parents[1] / "data" / "test_matrices"


def load_matrix(name):
    return np.loadtxt(MATRICES / name, delimiter=",", dtype=np.float32)


def vertical_edge(h=8, w=8, left=0.0, right=100.0):
    img = np.full((h, w), left, dtype=np.float32)
    img[:, w // 2:] = right
    return img


class TestSobelBasics(unittest.TestCase):
    def test_constant_image_gives_zero(self):
        for value in (0.0, 80.0, 255.0):
            img = np.full((6, 7), value, dtype=np.float32)
            gx, gy = sobel_gradients(img)
            m = sobel_magnitude(img)
            self.assertTrue(np.all(gx == 0) and np.all(gy == 0))
            self.assertTrue(np.all(m == 0))

    def test_shape_dtype_nonnegative(self):
        img = np.random.default_rng(0).uniform(0, 255, (9, 13)).astype(np.float32)
        m = sobel_magnitude(img)
        self.assertEqual(m.shape, img.shape)
        self.assertEqual(m.dtype, np.float32)
        self.assertTrue(np.all(m >= 0))

    def test_hand_computed_small_matrix(self):
        img = np.array([[0, 0, 10]] * 3, dtype=np.float32)
        gx, gy = sobel_gradients(img)
        expected_gx = np.array([[0, 40, 40]] * 3, dtype=np.float32)
        np.testing.assert_array_equal(gx, expected_gx)
        np.testing.assert_array_equal(gy, np.zeros((3, 3), dtype=np.float32))
        np.testing.assert_array_equal(sobel_magnitude(img), expected_gx)

    def test_vertical_edge_only_gx(self):
        gx, gy = sobel_gradients(vertical_edge())
        self.assertTrue(np.all(gy == 0))
        self.assertTrue(np.all(gx[:, 3:5] == 400))   # 4 * 100 tại hai cột sát cạnh
        self.assertTrue(np.all(gx[:, :3] == 0) and np.all(gx[:, 5:] == 0))

    def test_horizontal_edge_only_gy(self):
        gx, gy = sobel_gradients(vertical_edge().T.copy())
        self.assertTrue(np.all(gx == 0))
        self.assertTrue(np.all(gy[3:5, :] == 400))

    def test_sign_follows_intensity_increase(self):
        gx, _ = sobel_gradients(vertical_edge(left=0, right=100))
        gx_rev, _ = sobel_gradients(vertical_edge(left=100, right=0))
        self.assertTrue(np.all(gx >= 0))
        self.assertTrue(np.all(gx_rev <= 0))

    def test_magnitude_can_exceed_255(self):
        self.assertGreater(float(sobel_magnitude(vertical_edge()).max()), 255.0)

    def test_one_pixel_and_single_row(self):
        np.testing.assert_array_equal(
            sobel_magnitude(np.array([[5.0]], dtype=np.float32)), [[0.0]]
        )
        self.assertEqual(sobel_magnitude(np.ones((1, 5), dtype=np.float32)).shape, (1, 5))

    def test_does_not_modify_input(self):
        img = vertical_edge()
        before = img.copy()
        sobel_magnitude(img)
        np.testing.assert_array_equal(img, before)

    def test_accepts_integer_input(self):
        img = vertical_edge().astype(np.uint8)
        np.testing.assert_array_equal(
            sobel_magnitude(img), sobel_magnitude(img.astype(np.float32))
        )

    def test_kernels_are_cross_correlation_form(self):
        np.testing.assert_array_equal(SOBEL_KX, SOBEL_KY.T)
        self.assertEqual(float(SOBEL_KX.sum()), 0.0)  # vùng phẳng cho 0


class TestSharedMatrices(unittest.TestCase):
    """Dùng ma trận chung của nhóm trong data/test_matrices/."""

    def test_constant_5x5(self):
        self.assertTrue(np.all(sobel_magnitude(load_matrix("constant_5x5.csv")) == 0))

    def test_vertical_edge_7x7(self):
        gx, gy = sobel_gradients(load_matrix("vertical_edge_7x7.csv"))
        self.assertTrue(np.all(gy == 0))
        self.assertTrue(np.all(gx[:, 2:4] == 1020))  # 4 × 255 tại hai cột sát cạnh
        self.assertTrue(np.all(gx[:, :2] == 0) and np.all(gx[:, 4:] == 0))

    def test_horizontal_edge_7x7(self):
        gx, gy = sobel_gradients(load_matrix("horizontal_edge_7x7.csv"))
        self.assertTrue(np.all(gx == 0))
        self.assertTrue(np.all(gy[2:4, :] == 1020))
        self.assertTrue(np.all(gy[:2, :] == 0) and np.all(gy[4:, :] == 0))

    def test_impulse_5x5_is_symmetric_and_local(self):
        m = sobel_magnitude(load_matrix("impulse_5x5.csv"))
        self.assertEqual(float(m[2, 2]), 0.0)          # tâm: hai bên bằng nhau
        self.assertTrue(np.all(m[0, :] == 0) and np.all(m[:, 0] == 0))  # cách xa xung
        np.testing.assert_allclose(m, m[::-1, ::-1], atol=1e-4)         # đối xứng tâm


class TestSobelErrors(unittest.TestCase):
    def test_invalid_inputs_raise_value_error(self):
        bad = [
            [[1.0, 2.0]],                                   # không phải ndarray
            np.zeros((3, 3, 3), dtype=np.float32),          # 3 chiều
            np.zeros(5, dtype=np.float32),                  # 1 chiều
            np.zeros((0, 4), dtype=np.float32),             # rỗng
            np.zeros((3, 3), dtype=bool),                   # bool
            np.array([["a", "b"]]),                         # không phải số
            np.array([[1.0, np.nan]], dtype=np.float32),    # NaN
            np.array([[1.0, np.inf]], dtype=np.float32),    # inf
        ]
        for item in bad:
            with self.subTest(item=repr(item)[:30]):
                with self.assertRaises(ValueError):
                    sobel_magnitude(item)


@unittest.skipIf(cv2 is None, "Chưa cài OpenCV")
class TestSobelVsOpenCV(unittest.TestCase):
    """Đối chiếu Gx, Gy trước, rồi mới đến M (cùng ảnh float32, BORDER_REPLICATE)."""

    def _cv(self, img):
        kw = dict(ksize=3, borderType=cv2.BORDER_REPLICATE)
        return (cv2.Sobel(img, cv2.CV_32F, 1, 0, **kw),
                cv2.Sobel(img, cv2.CV_32F, 0, 1, **kw))

    def test_matches_opencv(self):
        rng = np.random.default_rng(42)
        cases = {
            "ngau_nhien": rng.uniform(0, 255, (31, 47)).astype(np.float32),
            "canh_doc": vertical_edge(),
            "canh_ngang": vertical_edge().T.copy(),
            "hang": np.full((10, 10), 80, dtype=np.float32),
        }
        for name, img in cases.items():
            with self.subTest(name):
                gx, gy = sobel_gradients(img)
                cx, cy = self._cv(img)
                np.testing.assert_allclose(gx, cx, atol=1e-3)
                np.testing.assert_allclose(gy, cy, atol=1e-3)
                np.testing.assert_allclose(
                    sobel_magnitude(img), cv2.magnitude(cx, cy), atol=1e-3
                )


@unittest.skipIf(cv2 is None, "Chưa cài OpenCV")
class TestReferenceBranch(unittest.TestCase):
    def test_reference_functions_match_main_branch(self):
        from evaluation.reference import reference_sobel_magnitude
        from evaluation.sobel_compare import compare_sobel

        img = np.random.default_rng(7).uniform(0, 255, (20, 30)).astype(np.float32)
        np.testing.assert_allclose(
            sobel_magnitude(img), reference_sobel_magnitude(img), atol=1e-3
        )
        stats = compare_sobel(img)
        self.assertLess(stats["magnitude_max"], 1e-3)


if __name__ == "__main__":
    unittest.main()
