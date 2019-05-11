from unittest import TestCase
from .displayio_shared_bindings import Bitmap_C_Interface


class TestBitmap_C(TestCase):
    def test_init(self):
        b = Bitmap_C_Interface(2, 4, 1)
        self.assertEqual(2, b.width)
        self.assertEqual(4, b.height)
        self.assertEqual(1, b.colors)

    def test_abs(self):
        b = Bitmap_C_Interface(5, 2, 1)
        self.assertEqual(9, b._abs_pos(4, 1))

    def test_set_tuple(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[1, 3] = 67
        self.assertEqual(b[1, 3], 67)

    def test_set_abs(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[0] = 42
        self.assertEqual(b[0], 42)

    def test_abs_and_tuple(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[7] = 101
        self.assertEqual(101, b[1, 3])

    def test_non_zero(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[1, 1] = 100
        self.assertEqual(100, b[1, 1])

    def test_throws_x_out_of_range(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b[2, 1] = 100
            self.fail("should have thrown")
        except ValueError:
            pass

    def test_max(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[1, 1] = 66
        self.assertEqual(66, b[1, 1])

    def test_uninitialized(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b[1, 1]
            self.fail("should have thrown")
        except RuntimeError:
            pass

    def test_validate_throws(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b.validate()
        except ValueError:
            pass

    def test_repr(self):
        b = Bitmap_C_Interface(3, 2, 1)
        b[0, 0] = 1
        b[1, 0] = 0
        b[2, 0] = 0
        b[0, 1] = 1
        b[1, 1] = 1
        b[2, 1] = 0
        self.assertEqual("\n   1   0   0\n   1   1   0\n", str(b))

    def test_decode(self):
        b = Bitmap_C_Interface(4, 4, 1)
        self.assertEqual((0, 0), b._decode(0))
        encoded = b._abs_pos(3, 3)
        self.assertEqual((3, 3), b._decode(encoded))
