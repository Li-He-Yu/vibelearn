# -*- coding: utf-8 -*-
"""Extract PDF text into the project's configured cache with a manifest.

Usage:
  python vibelearn/scripts/extract_pdf_to_cache.py <path-to-pdf> [--force]

Outputs:
  <configured pdf_text_cache_dir>/<pdf-stem>.txt
  <configured manifest_dir>/<pdf-stem>.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from config_utils import find_project_root, get_nested, load_project_config, resolve_project_path


@dataclass
class ExtractionResult:
    extractor: str
    text: str
    page_count: int | None
    warnings: list[str]


def _resolve_pdf_path(raw_path: str, project_root: Path) -> Path:
    pdf_path = Path(raw_path)
    if not pdf_path.is_absolute():
        pdf_path = project_root / pdf_path
    return pdf_path.resolve()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _cache_paths(project_root: Path, project_config: dict[str, object], pdf_path: Path) -> tuple[Path, Path]:
    text_dir = resolve_project_path(
        project_root,
        get_nested(project_config, "paths", "pdf_text_cache_dir"),
        "./vlcache/pdf_text",
    )
    manifest_dir = resolve_project_path(
        project_root,
        get_nested(project_config, "paths", "manifest_dir"),
        "./vlcache/manifests",
    )
    text_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    return text_dir / f"{pdf_path.stem}.txt", manifest_dir / f"{pdf_path.stem}.json"


def _is_cache_fresh(pdf_path: Path, manifest_path: Path, text_path: Path, source_hash: str) -> bool:
    if not manifest_path.exists() or not text_path.exists():
        return False
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return (
        data.get("source_path") == str(pdf_path)
        and data.get("source_sha256") == source_hash
        and data.get("output_text_path") == str(text_path)
    )


def _extract_with_pymupdf(pdf_path: Path) -> ExtractionResult | None:
    try:
        import fitz
    except Exception:
        return None

    doc = fitz.open(pdf_path)
    try:
        parts: list[str] = []
        for page_num, page in enumerate(doc, start=1):
            parts.append(f"\n\n--- Page {page_num} ---\n\n")
            parts.append(page.get_text("text"))
        return ExtractionResult("pymupdf", "".join(parts), doc.page_count, [])
    finally:
        doc.close()


def _extract_with_pdfplumber(pdf_path: Path) -> ExtractionResult | None:
    try:
        import pdfplumber
    except Exception:
        return None

    with pdfplumber.open(pdf_path) as pdf:
        parts: list[str] = []
        for page_num, page in enumerate(pdf.pages, start=1):
            parts.append(f"\n\n--- Page {page_num} ---\n\n")
            parts.append(page.extract_text() or "")
        return ExtractionResult("pdfplumber", "".join(parts), len(pdf.pages), [])


def _extract_with_pypdf(pdf_path: Path) -> ExtractionResult | None:
    for module_name in ("pypdf", "PyPDF2"):
        try:
            mod = __import__(module_name)
        except Exception:
            continue

        reader = mod.PdfReader(str(pdf_path))
        parts: list[str] = []
        for page_num, page in enumerate(reader.pages, start=1):
            parts.append(f"\n\n--- Page {page_num} ---\n\n")
            parts.append(page.extract_text() or "")
        return ExtractionResult(module_name, "".join(parts), len(reader.pages), [])

    return None


def _extract_with_pdftotext(pdf_path: Path) -> ExtractionResult | None:
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None

    if proc.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {proc.stderr.strip()}")

    return ExtractionResult("pdftotext", proc.stdout, None, [])


def _extract_text(pdf_path: Path) -> ExtractionResult:
    extractors: list[Callable[[Path], ExtractionResult | None]] = [
        _extract_with_pymupdf,
        _extract_with_pdfplumber,
        _extract_with_pypdf,
        _extract_with_pdftotext,
    ]

    errors: list[str] = []
    for extractor in extractors:
        try:
            result = extractor(pdf_path)
        except Exception as exc:
            errors.append(f"{extractor.__name__}: {exc}")
            continue
        if result and result.text.strip():
            return result
        if result:
            errors.append(f"{extractor.__name__}: empty output")

    raise RuntimeError("No PDF extractor succeeded. " + "; ".join(errors))


def _detect_suspicious_output(text: str, page_count: int | None) -> list[str]:
    warnings: list[str] = []
    stripped = text.strip()
    if len(stripped) < 200:
        warnings.append("very_short_text")
    if page_count and len(stripped) / max(page_count, 1) < 80:
        warnings.append("low_text_density")
    if "\x0c" in text:
        warnings.append("form_feed_detected")
    return warnings


def _write_manifest(
    manifest_path: Path,
    pdf_path: Path,
    text_path: Path,
    source_hash: str,
    result: ExtractionResult,
) -> None:
    stat = pdf_path.stat()
    warnings = list(result.warnings)
    warnings.extend(_detect_suspicious_output(result.text, result.page_count))

    manifest = {
        "schema_version": 1,
        "source_path": str(pdf_path),
        "source_sha256": source_hash,
        "source_size_bytes": stat.st_size,
        "source_mtime_utc": _utc_iso(stat.st_mtime),
        "extracted_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "extractor": result.extractor,
        "page_count": result.page_count,
        "char_count": len(result.text),
        "warnings": warnings,
        "output_text_path": str(text_path),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Extract PDF text into the configured cache")
    parser.add_argument("pdf_path", help="Path to the PDF, relative to repo root or absolute")
    parser.add_argument("--force", action="store_true", help="Re-extract even if cache manifest is fresh")
    args = parser.parse_args(argv[1:])

    project_root = find_project_root()
    project_config = load_project_config(project_root)
    pdf_path = _resolve_pdf_path(args.pdf_path, project_root)
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        print(f"Not a PDF or not found: {pdf_path}")
        return 2

    text_path, manifest_path = _cache_paths(project_root, project_config, pdf_path)
    source_hash = _sha256(pdf_path)
    if not args.force and _is_cache_fresh(pdf_path, manifest_path, text_path, source_hash):
        try:
            print(str(text_path.relative_to(project_root)))
        except ValueError:
            print(str(text_path))
        return 0

    result = _extract_text(pdf_path)
    text_path.write_text(result.text, encoding="utf-8", newline="\n")
    _write_manifest(manifest_path, pdf_path, text_path, source_hash, result)
    try:
        print(str(text_path.relative_to(project_root)))
    except ValueError:
        print(str(text_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
