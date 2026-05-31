# -*- coding: utf-8 -*-
"""Create a project-level vibelearn config from the bundled example.

Usage:
  python vibelearn/scripts/init_project_config.py [target-dir] [--force]

Default output:
  ./vibelearn.config.yaml
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from config_utils import CONFIG_FILENAME


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=f"Initialize a {CONFIG_FILENAME} in a project")
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help=f"Project root directory that should receive {CONFIG_FILENAME}",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config file")
    args = parser.parse_args(argv[1:])

    skill_root = _skill_root()
    source = skill_root / "assets" / "example-vibelearn.config.yaml"
    target_dir = Path(args.target_dir)
    if not target_dir.is_absolute():
        target_dir = (Path.cwd() / target_dir).resolve()

    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / CONFIG_FILENAME

    if target.exists() and not args.force:
        print(f"Config already exists: {target}")
        print("Use --force to overwrite it.")
        return 1

    shutil.copyfile(source, target)
    print(str(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
