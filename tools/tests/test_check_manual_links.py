import tempfile
import unittest
from pathlib import Path

from tools.check_manual_links import broken_links

MANUAL = '<a id="s21"></a>\n## Sivu 21\n'


class BrokenLinksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("manuals/kasikirja.md", MANUAL)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, text):
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).write_text(text)
        return path

    def test_a_doc_link_to_a_page_anchor_resolves(self):
        doc = self.write("docs/controller.md", "See [p. 21](../manuals/kasikirja.md#s21).\n")
        self.assertEqual(broken_links(self.root, [doc]), [])

    def test_a_doc_link_to_a_missing_page_anchor_is_broken(self):
        doc = self.write("docs/controller.md", "Intro.\nSee [p. 99](../manuals/kasikirja.md#s99).\n")
        self.assertEqual(
            broken_links(self.root, [doc]), [("docs/controller.md", 2, "../manuals/kasikirja.md#s99")]
        )

    def test_a_link_to_a_missing_manual_is_broken(self):
        doc = self.write("docs/controller.md", "See [p. 21](../manuals/kaesikirja.md#s21).\n")
        self.assertEqual(
            broken_links(self.root, [doc]), [("docs/controller.md", 1, "../manuals/kaesikirja.md#s21")]
        )

    def test_a_link_that_names_a_manual_from_the_wrong_folder_is_broken(self):
        doc = self.write("docs/controller.md", "See [p. 21](kasikirja.md#s21).\n")
        self.assertEqual(broken_links(self.root, [doc]), [("docs/controller.md", 1, "kasikirja.md#s21")])

    def test_a_link_outside_the_manuals_is_not_checked(self):
        self.write("docs/adr/0004-entity-ids.md", "# Entity IDs stay stable\n")
        doc = self.write("docs/controller.md", "See [ADR 0004](adr/0004-entity-ids.md#entity-ids-stay-stable).\n")
        self.assertEqual(broken_links(self.root, [doc]), [])

    def test_a_code_comment_cites_from_the_repo_root(self):
        code = self.write(
            "components/geopro_202s/register_map.py",
            "# Kompr.esto (manuals/kasikirja.md#s21)\n# VaraajaYlä (manuals/kasikirja.md#s20)\n",
        )
        self.assertEqual(
            broken_links(self.root, [code]),
            [("components/geopro_202s/register_map.py", 2, "manuals/kasikirja.md#s20")],
        )


if __name__ == "__main__":
    unittest.main()
