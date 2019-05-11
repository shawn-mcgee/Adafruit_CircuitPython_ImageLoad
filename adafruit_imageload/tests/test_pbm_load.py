import os
from io import BytesIO
from unittest import TestCase
from adafruit_imageload import pnm
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestPnmLoad(TestCase):
    def test_load_fails_with_no_header_data(self):
        f = BytesIO(b"some initial binary data: \x00\x01")
        try:
            pnm.load(f, b"P1", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface)
            self.fail("should have failed")
        except Exception as e:
            if "Unsupported image format" not in str(e):
                raise

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p1_mono_ascii.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(
                f, b"P1", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(13, bitmap.width)
        self.assertEqual(21, bitmap.height)

        bitmap.validate()
        self.assertEqual(0, bitmap[0])  # check first row
        self.assertEqual(1, bitmap[11, 1])  # check second row

        self.assertEqual(1, palette.num_colors)
        palette.validate()

    def test_load_works_p4_in_mem(self):
        f = BytesIO(b"P4\n4 2\n\x55")
        bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertEqual(4, bitmap.width)
        self.assertEqual(2, bitmap.height)
        bitmap.validate()
        self.assertEqual("\n   1   0   1   0\n   1   0   1   0\n", str(bitmap))

    def test_load_works_p4_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p4_mono_binary.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(32, bitmap.width)
        self.assertEqual(15, bitmap.height)
        bitmap.validate()

    def test_load_works_p4_binary_high_res(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p4_mono_large.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(320, bitmap.width)
        self.assertEqual(240, bitmap.height)
