"""Phát hiện biên bằng toán tử Sobel (tự cài đặt bằng NumPy).

Phụ trách: Long.

Quy ước (khớp kế hoạch nhóm):
  * Đầu vào  : ảnh mức xám H×W, số thực hữu hạn (thường float32, 0–255).
  * Rìa ảnh  : np.pad(mode="edge"), tương ứng cv2.BORDER_REPLICATE.
  * Phép tính: tương quan (không lật kernel), tương ứng cv2.Sobel / cv2.filter2D.
  * Đầu ra   : float32, cùng kích thước H×W. Độ lớn M là giá trị THÔ,
               có thể lớn hơn 255; không chuẩn hóa ở đây.
  * Không sửa mảng đầu vào, không mở hộp thoại, không ghi tệp.
"""

from __future__ import annotations

import numpy as np

# Gx dương khi cường độ tăng sang phải (+x); Gy dương khi tăng đi xuống (+y).
# Trùng với cv2.Sobel(dx=1, dy=0) và cv2.Sobel(dx=0, dy=1), ksize=3.
SOBEL_KX = np.array([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]], dtype=np.float32)
SOBEL_KY = np.array([[-1, -2, -1],
                     [0, 0, 0],
                     [1, 2, 1]], dtype=np.float32)


def _validate_gray(gray: np.ndarray) -> np.ndarray:
    """Kiểm tra đầu vào và trả về bản sao float32 (không sửa mảng gốc)."""
    if not isinstance(gray, np.ndarray):
        raise ValueError("Ảnh mức xám phải là mảng NumPy.")
    if gray.ndim != 2:
        raise ValueError(
            f"Ảnh mức xám phải có dạng H×W (2 chiều), nhận được {gray.ndim} chiều."
        )
    if gray.shape[0] < 1 or gray.shape[1] < 1:
        raise ValueError("Ảnh mức xám không được rỗng.")
    if gray.dtype == np.bool_ or not np.issubdtype(gray.dtype, np.number):
        raise ValueError(f"Ảnh mức xám phải là kiểu số, nhận được {gray.dtype}.")
    out = gray.astype(np.float32, copy=True)
    if not np.all(np.isfinite(out)):
        raise ValueError("Ảnh mức xám chứa NaN hoặc vô cùng.")
    return out


def sobel_gradients(gray: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Tính (Gx, Gy) của Sobel 3×3, mỗi mảng H×W float32, có dấu.

    Dùng để đối chiếu từng thành phần với cv2.Sobel trước khi xem tranh cuối.
    """
    g = _validate_gray(gray)
    h, w = g.shape
    p = np.pad(g, 1, mode="edge")  # (H+2)×(W+2), lặp giá trị rìa

    # t[r][c]: ảnh dịch ứng với ô (r, c) của kernel 3×3.
    t = [[p[r:r + h, c:c + w] for c in range(3)] for r in range(3)]

    # Tương quan với SOBEL_KX / SOBEL_KY, viết tường minh để dễ đối chiếu công thức.
    gx = (t[0][2] - t[0][0]) + 2.0 * (t[1][2] - t[1][0]) + (t[2][2] - t[2][0])
    gy = (t[2][0] - t[0][0]) + 2.0 * (t[2][1] - t[0][1]) + (t[2][2] - t[0][2])
    return gx.astype(np.float32), gy.astype(np.float32)


def sobel_magnitude(gray: np.ndarray) -> np.ndarray:
    """Độ lớn gradient thô M = sqrt(Gx² + Gy²); H×W, float32, không âm."""
    gx, gy = sobel_gradients(gray)
    return np.sqrt(gx * gx + gy * gy).astype(np.float32)