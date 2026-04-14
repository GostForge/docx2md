import unittest

from core.converter import DocxToMdConverter


class TestConverterPathSanitization(unittest.TestCase):
    def setUp(self):
        self.converter = DocxToMdConverter(extract_media_path="/tmp/work/media")

    def test_sanitizes_absolute_posix_media_path(self):
        content = "![](/tmp/tmpbzwqhz78/media/media/image2.png)"
        sanitized = self.converter._sanitize_media_links(content)
        self.assertEqual(sanitized, "![](media/image2.png)")

    def test_sanitizes_single_media_prefix(self):
        content = "![](/tmp/tmpbzwqhz78/media/image2.png)"
        sanitized = self.converter._sanitize_media_links(content)
        self.assertEqual(sanitized, "![](media/image2.png)")

    def test_sanitizes_windows_absolute_media_path(self):
        content = "![](C:\\tmp\\tmpbzwqhz78\\media\\media\\image2.png)"
        sanitized = self.converter._sanitize_media_links(content)
        self.assertEqual(sanitized, "![](media/image2.png)")

    def test_keeps_external_links_unchanged(self):
        content = "![](https://example.com/img.png)"
        sanitized = self.converter._sanitize_media_links(content)
        self.assertEqual(sanitized, content)


if __name__ == "__main__":
    unittest.main()
