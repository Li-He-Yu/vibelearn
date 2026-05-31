# -*- coding: utf-8 -*-
"""Compatibility wrapper for the canonical PDF cache extractor.

Usage:
  python vibelearn/scripts/pdf_to_text.py <path-to-pdf> [--force]

Outputs:
  <configured pdf_text_cache_dir>/<pdf-stem>.txt
  <configured manifest_dir>/<pdf-stem>.json
"""

from __future__ import annotations

import sys

from extract_pdf_to_cache import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
