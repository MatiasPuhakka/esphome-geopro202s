# Tests the Component revision that codegen stamps into the firmware, against
# throwaway git repos. `make test` runs it.
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'components' / 'geopro_202s'))
from revision import component_revision  # noqa: E402

GIT_IDENTITY = {
    'GIT_AUTHOR_NAME': 'test',
    'GIT_AUTHOR_EMAIL': 'test@example.com',
    'GIT_COMMITTER_NAME': 'test',
    'GIT_COMMITTER_EMAIL': 'test@example.com',
}


def git(repo, *args):
    result = subprocess.run(['git', *args], cwd=repo, env={**os.environ, **GIT_IDENTITY},
                            check=True, capture_output=True, text=True)
    return result.stdout.strip()


class ComponentRevisionTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.component = self.root / 'components' / 'geopro_202s'
        self.component.mkdir(parents=True)
        (self.component / '__init__.py').write_text('a\n')
        (self.root / '.gitignore').write_text('__pycache__/\n')
        git(self.root, 'init', '-q')
        git(self.root, 'add', '.')
        git(self.root, 'commit', '-q', '-m', 'one')
        self.head = git(self.root, 'rev-parse', 'HEAD')

    def assertRevisionOf(self, revision, dirty=False):
        commit, _, suffix = revision.partition('-')
        self.assertGreaterEqual(len(commit), 7, revision)
        self.assertTrue(self.head.startswith(commit), revision)
        self.assertEqual(suffix, 'dirty' if dirty else '', revision)

    def test_clean_checkout_gives_the_head_commit(self):
        self.assertRevisionOf(component_revision(self.component))

    def test_modified_component_file_marks_dirty(self):
        (self.component / '__init__.py').write_text('b\n')
        self.assertRevisionOf(component_revision(self.component), dirty=True)

    def test_untracked_component_file_marks_dirty(self):
        # ESPHome compiles every source file in the Component's directory.
        (self.component / 'extra.cpp').write_text('')
        self.assertRevisionOf(component_revision(self.component), dirty=True)

    def test_changes_outside_the_component_leave_it_clean(self):
        (self.root / 'geopro.yaml').write_text('x\n')
        self.assertRevisionOf(component_revision(self.component))

    def test_ignored_files_leave_it_clean(self):
        # Python writes __pycache__ next to __init__.py when ESPHome imports it.
        (self.component / '__pycache__').mkdir()
        (self.component / '__pycache__' / 'revision.pyc').write_text('')
        self.assertRevisionOf(component_revision(self.component))

    def test_shallow_clone_gives_its_head_commit(self):
        # The add-on's github:// source is a `git clone --depth=1`.
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        clone = Path(tmp.name) / 'clone'
        git(tmp.name, 'clone', '-q', '--depth=1', self.root.as_uri(), str(clone))
        self.assertRevisionOf(component_revision(clone / 'components' / 'geopro_202s'))

    def test_directory_outside_git_is_unknown(self):
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(component_revision(Path(outside)), 'unknown')

    def test_missing_git_is_unknown(self):
        self.assertEqual(component_revision(self.component, git='no-such-git'), 'unknown')


if __name__ == '__main__':
    unittest.main()
