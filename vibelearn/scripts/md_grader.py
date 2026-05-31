# -*- coding: utf-8 -*-
"""Inline grader helper for markdown tests.

This is a generic, reusable scaffold.
- Reads/writes UTF-8.
- Avoids emoji markers (uses OK/NG) to prevent cp950 console issues.

Typical workflow:
  1) Copy this script and customize `feedback` for a specific test, OR
  2) Extend it to parse an answer key and auto-grade.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from config_utils import find_project_root


def remove_previous_grading(text: str) -> str:
    return re.sub(r"(?m)^【批改】.*(?:\n^【(?:正解|解析|回覆)】.*)*\n?", "", text)


def grade_file(path: Path, feedback: dict[int, str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = remove_previous_grading(text)

    pattern = re.compile(r"(?m)^\*\*(\d+)\.\*\*")
    matches = list(pattern.finditer(text))
    if not matches:
        raise SystemExit("No question headers (**n.**) found.")

    out_parts: list[str] = []
    for idx, match in enumerate(matches):
        qn = int(match.group(1))
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end]

        fb = feedback.get(qn)
        if not fb:
            out_parts.append(block)
            continue

        if not block.endswith("\n"):
            block += "\n"
        block += "\n" + fb.strip() + "\n\n"
        out_parts.append(block)

    new_text = text[: matches[0].start()] + "".join(out_parts)
    path.write_text(new_text, encoding="utf-8", newline="\n")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python vibelearn/scripts/md_grader.py <path-to-md>")
        return 2

    project_root = find_project_root()
    md_path = Path(argv[1])
    if not md_path.is_absolute():
        md_path = project_root / md_path

    if not md_path.exists() or md_path.suffix.lower() != ".md":
        print(f"Not a markdown file or not found: {md_path}")
        return 2

    # TODO: fill with real feedback per file.
    feedback: dict[int, str] = {
        # 1: "【批改】OK  ",
        # 2: "【批改】NG  \n【正解】...  \n【解析】...  ",
    }

    grade_file(md_path, feedback)
    print(f"graded: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
