# -*- coding: utf-8 -*-
"""Small helpers for reading the project-level vibelearn config."""

from __future__ import annotations

from pathlib import Path
from typing import Any


CONFIG_FILENAME = "vibelearn.config.yaml"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / CONFIG_FILENAME).exists():
            return candidate
    return current


def load_project_config(project_root: Path) -> dict[str, Any]:
    config_path = project_root / CONFIG_FILENAME
    if not config_path.exists():
        return {}
    return _parse_simple_yaml(config_path.read_text(encoding="utf-8"))


def resolve_project_path(project_root: Path, raw_path: str | None, default_relative: str) -> Path:
    selected = raw_path or default_relative
    path = Path(selected)
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def get_nested(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        line = _strip_comment(raw_line)
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]
        if not value:
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue

        parent[key] = _parse_scalar(value)

    return root


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    chars: list[str] = []

    for ch in line:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            break
        chars.append(ch)

    return "".join(chars).rstrip()


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
