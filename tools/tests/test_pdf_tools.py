"""The PDF tools read the manuals with PDFKit, which only macOS has, so these tests skip elsewhere,
CI included. They run each script as an executable, as docs/agents/manual-transcription.md does."""
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF_TEXT = ROOT / "tools" / "pdf_text.js"
PDF_PNG = ROOT / "tools" / "pdf_png.js"
KASIKIRJA = ROOT / "manuals" / "Geopro 202S Käsikirja.pdf"

ON_MACOS = sys.platform == "darwin" and shutil.which("osascript") is not None


def run(script, *args, cwd=None):
    return subprocess.run([script, *map(str, args)], cwd=cwd, capture_output=True, text=True)


def markers(stdout):
    return [line for line in stdout.splitlines() if line.startswith("=====")]


def png_size(path):
    """The width and height in a PNG's header."""
    data = path.read_bytes()[:24]
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), f"{path} is not a PNG"
    return struct.unpack(">II", data[16:24])


@unittest.skipUnless(ON_MACOS, "PDFKit is macOS only")
class PdfTextTest(unittest.TestCase):
    def test_without_arguments_it_prints_its_usage(self):
        result = run(PDF_TEXT)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr.startswith("usage: tools/pdf_text.js <pdf> <page>..."), result.stderr)

    def test_it_prints_only_the_page_asked_for_under_its_marker(self):
        result = run(PDF_TEXT, KASIKIRJA, 22)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(markers(result.stdout), ["===== PAGE 22 / 44 ====="])
        self.assertTrue(result.stdout.startswith("===== PAGE 22 / 44 =====\n"))
        self.assertIn("Esimerkki 1. Maalämpökojeen ohjaus", result.stdout)
        self.assertNotIn("ASETUSARVOT, käyttäjätaso", result.stdout)  # p. 21
        self.assertNotIn("KOMPRESSORIN KÄYNNIN OHJAUS", result.stdout)  # p. 23

    def test_a_range_prints_each_of_its_pages_in_order(self):
        result = run(PDF_TEXT, KASIKIRJA, "21-23", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            markers(result.stdout),
            [
                "===== PAGE 21 / 44 =====",
                "===== PAGE 22 / 44 =====",
                "===== PAGE 23 / 44 =====",
                "===== PAGE 2 / 44 =====",
            ],
        )
        page_23 = result.stdout.split("===== PAGE 23 / 44 =====")[1].split("===== PAGE 2 / 44 =====")[0]
        self.assertIn("KOMPRESSORIN KÄYNNIN OHJAUS", page_23)

    def test_a_page_without_a_text_layer_says_so(self):
        result = run(PDF_TEXT, KASIKIRJA, 43)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "===== PAGE 43 / 44 =====\n(no text layer)\n")

    def test_a_relative_pdf_path_is_read_from_the_working_directory(self):
        result = run(PDF_TEXT, KASIKIRJA.name, 22, cwd=KASIKIRJA.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Esimerkki 1. Maalämpökojeen ohjaus", result.stdout)

    def test_a_page_past_the_end_fails_and_names_the_page_count(self):
        result = run(PDF_TEXT, KASIKIRJA, "43-45")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("page 45 is outside the PDF's 44 pages", result.stderr)

    def test_an_argument_that_is_not_a_page_or_range_fails_with_the_usage(self):
        for arg in ["p22", "23-21", "0", "21-"]:
            with self.subTest(arg=arg):
                result = run(PDF_TEXT, KASIKIRJA, arg)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn(f"{arg} is not a page or a range", result.stderr)
                self.assertIn("usage: tools/pdf_text.js", result.stderr)

    def test_a_file_that_is_not_a_pdf_fails(self):
        result = run(PDF_TEXT, ROOT / "manuals" / "kasikirja.md", 1)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("can't open", result.stderr)


@unittest.skipUnless(ON_MACOS, "PDFKit is macOS only")
class PdfPngTest(unittest.TestCase):
    def test_without_arguments_it_prints_its_usage(self):
        result = run(PDF_PNG)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(
            result.stderr.startswith("usage: tools/pdf_png.js <pdf> <outdir> <scale> <page>..."), result.stderr
        )

    def test_it_renders_a_page_at_the_scale_asked_for(self):
        with tempfile.TemporaryDirectory() as out:
            result = run(PDF_PNG, KASIKIRJA, out, 2, 22)
            self.assertEqual(result.returncode, 0, result.stderr)
            png = Path(out) / "page-22.png"
            # The Käsikirja's pages are A4, 595 x 842 points.
            self.assertEqual(png_size(png), (1190, 1684))
            self.assertEqual(result.stdout, f"{png} 1190x1684\n")

    def test_a_range_renders_each_page_into_a_new_folder_under_the_working_directory(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = run(PDF_PNG, KASIKIRJA, "renders/kasikirja", 1, "21-22", cwd=cwd)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout,
                "renders/kasikirja/page-21.png 595x842\nrenders/kasikirja/page-22.png 595x842\n",
            )
            for page in (21, 22):
                self.assertEqual(png_size(Path(cwd) / "renders" / "kasikirja" / f"page-{page}.png"), (595, 842))

    def test_a_bad_scale_or_page_fails_with_the_usage_and_writes_nothing(self):
        for scale, page, error in [
            ("x", "22", "x is not a scale"),
            ("0", "22", "0 is not a scale"),
            ("2", "p22", "p22 is not a page or a range"),
            ("2", "23-21", "23-21 is not a page or a range"),
        ]:
            with self.subTest(scale=scale, page=page), tempfile.TemporaryDirectory() as out:
                result = run(PDF_PNG, KASIKIRJA, out, scale, page)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(error, result.stderr)
                self.assertIn("usage: tools/pdf_png.js", result.stderr)
                self.assertEqual(list(Path(out).iterdir()), [])

    def test_a_page_past_the_end_fails_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as out:
            result = run(PDF_PNG, KASIKIRJA, out, 1, "44-45")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("page 45 is outside the PDF's 44 pages", result.stderr)
            self.assertEqual(list(Path(out).iterdir()), [])

    def test_a_file_that_is_not_a_pdf_fails(self):
        with tempfile.TemporaryDirectory() as out:
            result = run(PDF_PNG, ROOT / "manuals" / "kasikirja.md", out, 1, 1)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("can't open", result.stderr)


if __name__ == "__main__":
    unittest.main()
