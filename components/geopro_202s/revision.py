# The Component's git revision, which codegen stamps into the firmware.
# No ESPHome imports, so tests/test_revision.py can load it on its own.
import subprocess

UNKNOWN = 'unknown'


def component_revision(directory, git='git'):
    """Return the short commit checked out at `directory`, with '-dirty' appended
    when a file under `directory` is modified or untracked, or 'unknown' when git
    can't tell (git missing, or `directory` not tracked by a repository).

    Both build paths are git checkouts: a local build runs from this repository,
    and ESPHome fetches a github:// source with `git clone --depth=1`.
    """
    try:
        # A copy inside some other repository would report that repository's commit.
        if not _git(git, directory, 'ls-files', '--', '.'):
            return UNKNOWN
        commit = _git(git, directory, 'rev-parse', '--short', 'HEAD')
        # Only changes under the Component's directory reach the firmware, and
        # ESPHome compiles untracked source files there too.
        changes = _git(git, directory, 'status', '--porcelain', '--', '.')
    except (OSError, subprocess.SubprocessError):
        return UNKNOWN
    return commit + '-dirty' if changes else commit


def _git(git, directory, *args):
    result = subprocess.run([git, *args], cwd=directory, check=True, capture_output=True,
                            text=True, timeout=10)
    return result.stdout.strip()
