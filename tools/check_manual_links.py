"""Check that every link to a manual page anchor resolves (ADR 0006).

Prints file:line and the link for each one whose manual or anchor doesn't exist, and exits with
status 1 if there was one."""
import re
import subprocess
import sys
from pathlib import Path

# A link to an anchor in a Markdown file: the path up to ".md", then "#" and the anchor.
LINK = re.compile(r"[^\s()\[\]<>\"'`]+\.md#[\w-]+")
ANCHOR = re.compile(r'id="([\w-]+)"')


def broken_links(root, paths):
    """The (path, line number, link) of each link in the files at paths, relative to root, that
    points into manuals/ at a file or anchor that doesn't exist."""
    manuals = (root / "manuals").resolve()
    broken = []
    for path in paths:
        # Markdown links resolve from the file's folder, as GitHub renders them. Comments in code
        # name paths from the repo root.
        base = (root / path).parent if Path(path).suffix == ".md" else root
        for number, line in enumerate((root / path).read_text().splitlines(), 1):
            for link in LINK.findall(line):
                target, anchor = link.split("#")
                manual = (base / target).resolve()
                if not manual.is_relative_to(manuals):
                    # A manual's name reached by the wrong path, such as kasikirja.md from docs/.
                    if (manuals / manual.name).is_file():
                        broken.append((path, number, link))
                    continue
                if not manual.is_file() or anchor not in ANCHOR.findall(manual.read_text()):
                    broken.append((path, number, link))
    return broken


# The tracked files that cite manual pages: docs, code and configs. Skips the PDFs, images, JSON
# fixtures and traces, and this checker's tests, whose links are made up.
CITING_SUFFIXES = {".md", ".py", ".h", ".cpp", ".yaml", ".yml", ".txt"}
SKIPPED_PREFIX = "tools/tests/"


def main():
    root = Path(__file__).resolve().parent.parent
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.split("\0")
    citing = [
        path
        for path in tracked
        if Path(path).suffix in CITING_SUFFIXES and not path.startswith(SKIPPED_PREFIX)
    ]
    broken = broken_links(root, citing)
    for path, number, link in broken:
        print(f"{path}:{number}: {link} doesn't resolve")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
