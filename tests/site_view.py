"""Write site/ from the static export in out/, for the brief's tests. Standard library only.

The brief's acceptance tests read pages under site/ with `%BASE%` links and
the `%RELEASE%` marker, as in Yard Crew's static template. This maps each
exported page to that view with the same rule as Yard Crew's trusted build:
`href`/`src` values under NEXT_BASE_PATH become `%BASE%` links and the
release marker becomes `%RELEASE%`; Next.js's own error pages are left out.
Owner-owned, like every file under tests/.
"""

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERROR_PAGES = ("404.html", "_not-found.html")


def view(out, base, release):
    # `/<repo>/...` and, from `next/link` to "/", the bare `/<repo>`.
    root = r"/(?!/)" + (r'|(?=")' if base else "")
    attribute = re.compile(r'(\s(?:href|src)=")' + re.escape(base) + "(?:" + root + ")")
    found = {}
    for path in sorted(out.rglob("*")):
        name = path.relative_to(out).as_posix()
        if not path.is_file() or name in ERROR_PAGES:
            continue
        data = path.read_bytes()
        if name.endswith(".html"):
            text = attribute.sub(r"\1%BASE%", data.decode("utf-8"))
            data = text.replace(f'data-release="{release}"', 'data-release="%RELEASE%"').encode()
        found[name] = data
    return found


def main():
    site = ROOT / "site"
    shutil.rmtree(site, ignore_errors=True)
    base = os.environ.get("NEXT_BASE_PATH", "")
    release = os.environ.get("SITE_RELEASE", "local")
    for name, data in view(ROOT / "out", base, release).items():
        target = site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


if __name__ == "__main__":
    main()
