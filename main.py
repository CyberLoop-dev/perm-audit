#!/usr/bin/env python3
"""Read-only filesystem permission inventory."""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Entry:
    path: str
    kind: str
    mode: str
    octal: str
    size: int
    findings: list[str]


def inspect_entry(path: Path, st: os.stat_result) -> Entry:
    mode = stat.S_IMODE(st.st_mode)
    if stat.S_ISLNK(st.st_mode):
        kind = "symlink"
    elif stat.S_ISDIR(st.st_mode):
        kind = "directory"
    elif stat.S_ISREG(st.st_mode):
        kind = "file"
    else:
        kind = "other"

    findings: list[str] = []
    if mode & stat.S_IWOTH:
        findings.append("world-writable")
    if mode & stat.S_IWGRP:
        findings.append("group-writable")
    if kind == "file" and mode & 0o111:
        findings.append("executable")
    if mode & 0o700 == 0:
        findings.append("owner-no-access-bits")
    return Entry(
        path=str(path),
        kind=kind,
        mode=stat.filemode(st.st_mode),
        octal=f"{mode:04o}",
        size=st.st_size,
        findings=findings,
    )


def scan(root: Path, max_depth: int | None) -> tuple[list[Entry], list[str]]:
    results: list[Entry] = []
    errors: list[str] = []

    def visit(directory: Path, depth: int) -> None:
        try:
            with os.scandir(directory) as iterator:
                children = sorted(iterator, key=lambda item: item.name.casefold())
        except OSError as exc:
            errors.append(f"{directory}: {exc}")
            return

        for child in children:
            item = Path(child.path)
            try:
                st = child.stat(follow_symlinks=False)
            except OSError as exc:
                errors.append(f"{item}: {exc}")
                continue
            entry = inspect_entry(item, st)
            results.append(entry)
            if entry.kind == "directory" and (max_depth is None or depth < max_depth):
                visit(item, depth + 1)

    visit(root, 0)
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only permission audit; no files or permissions are changed."
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to inspect (default: .)")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a table")
    parser.add_argument("--all", action="store_true", help="Include entries with no findings")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum directory depth")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.max_depth is not None and args.max_depth < 0:
        parser.error("--max-depth must be zero or greater")

    entries, errors = scan(root, args.max_depth)
    shown = entries if args.all else [entry for entry in entries if entry.findings]

    if args.json:
        print(json.dumps({
            "root": str(root),
            "read_only": True,
            "platform_note": "Permission bits may be approximate on Windows." if os.name == "nt" else None,
            "scanned": len(entries),
            "findings": len([entry for entry in entries if entry.findings]),
            "entries": [asdict(entry) for entry in shown],
            "errors": errors,
        }, indent=2))
    else:
        print(f"Permission Audit · {root}")
        print(f"Scanned {len(entries)} entries · {sum(bool(e.findings) for e in entries)} with findings")
        if os.name == "nt":
            print("Note: Windows permission bits may be approximate.")
        if not shown:
            print("No permission findings.")
        for entry in shown:
            flags = ", ".join(entry.findings) if entry.findings else "no findings"
            print(f"{entry.mode} {entry.octal}  {entry.kind:9} {entry.size:>9}  {entry.path}  [{flags}]")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
