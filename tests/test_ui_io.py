"""Kiểm tra hàm sự kiện mở/lưu bằng hộp thoại giả lập, không tạo cửa sổ."""

from contextlib import ExitStack
import unittest
from unittest.mock import patch

import numpy as np

from ui import open_image_dialog, save_sketch_dialog


class UIDialogTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.parent = object()
        self.choose_open = self.stack.enter_context(patch('ui.filedialog.askopenfilename'))
        self.choose_save = self.stack.enter_context(patch('ui.filedialog.asksaveasfilename'))
        self.show_error = self.stack.enter_context(patch('ui.messagebox.showerror'))
        self.load = self.stack.enter_context(patch('ui.load_rgb'))
        self.save = self.stack.enter_context(patch('ui.save_sketch'))

    def test_open_cancel(self):
        self.choose_open.return_value = ''
        self.assertIsNone(open_image_dialog(self.parent))
        self.load.assert_not_called()
        self.show_error.assert_not_called()

    def test_open_success(self):
        self.choose_open.return_value = 'photo.png'
        self.load.return_value = np.zeros((1, 1, 3), np.uint8)
        self.assertIs(open_image_dialog(self.parent), self.load.return_value)
        self.load.assert_called_once_with('photo.png')
        self.show_error.assert_not_called()

    def test_open_error_shows_message(self):
        self.choose_open.return_value = 'bad.png'
        self.load.side_effect = OSError('cannot read')
        self.assertIsNone(open_image_dialog(self.parent))
        self.show_error.assert_called_once()

    def test_save_without_result(self):
        self.assertFalse(save_sketch_dialog(None, self.parent))
        self.choose_save.assert_not_called()
        self.save.assert_not_called()
        self.show_error.assert_called_once()

    def test_save_cancel(self):
        self.choose_save.return_value = ''
        self.assertFalse(save_sketch_dialog(np.zeros((1, 1), np.uint8), self.parent))
        self.save.assert_not_called()
        self.show_error.assert_not_called()

    def test_save_success(self):
        sketch = np.zeros((1, 1), np.uint8)
        self.choose_save.return_value = 'out.png'
        self.assertTrue(save_sketch_dialog(sketch, self.parent))
        self.save.assert_called_once_with('out.png', sketch)
        self.show_error.assert_not_called()

    def test_save_failure(self):
        self.choose_save.return_value = 'out.png'
        self.save.side_effect = OSError('cannot write')
        self.assertFalse(save_sketch_dialog(np.zeros((1, 1), np.uint8), self.parent))
        self.show_error.assert_called_once()


if __name__ == '__main__':
    unittest.main()
