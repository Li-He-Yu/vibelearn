# VibeLearn Architecture

## Layers

VibeLearn is split into three layers:

1. `vibelearn/`
   The reusable skill bundle: `SKILL.md`, scripts, references, assets, and UI metadata.
2. `vibelearn.config.yaml`
   A project-owned config file created inside a course-material repo.
3. `vlcache/`
   Runtime state owned by the project, not by the skill source repo.

This split keeps the skill reusable while still allowing per-project control over outputs, cache layout, templates, and style guidance.

## Design Goals

- Keep the skill bundle self-contained.
- Keep project-specific settings outside the skill bundle.
- Keep runtime cache out of git by default.
- Allow private templates and style references without requiring them to be published.
- Prefer deterministic helper scripts for cache extraction and writeback tasks.

## Key Extension Points

Project config can override:

- `templates.*`
  Use project-owned templates instead of the bundled defaults.
- `guidance.*`
  Use project-owned markdown references for subjective style rules.
- `generation.*`
  Provide lightweight density, answer-detail, and grading hints.

## Runtime Dependency Graph

```mermaid
graph TD
  SKILL["vibelearn/SKILL.md"]
  DEF["vibelearn/config/skill.defaults.yaml"]
  CFG["project/vibelearn.config.yaml"]

  WF["references/workflow.md"]
  OUT["references/output-rules.md"]
  QUAL["references/quality-rules.md"]
  ASSETS["assets/ASSETS.md"]

  EXTRACT["scripts/extract_pdf_to_cache.py"]
  INIT["scripts/init_project_config.py"]
  GRADER["scripts/md_grader.py"]

  TEMPL["bundled templates"]
  GUIDE["project guidance files"]
  CACHE["project cache directories"]

  SKILL --> DEF
  SKILL --> CFG
  SKILL --> WF
  SKILL --> OUT
  SKILL --> QUAL
  SKILL --> ASSETS

  DEF --> EXTRACT
  DEF --> INIT
  DEF --> GRADER
  DEF --> TEMPL

  CFG --> CACHE
  CFG --> GUIDE
  CFG --> TEMPL
```

## Publication Notes

This source repo is intended to stay clean:

- no course PDFs
- no personal note/test/answer output
- no checked-in runtime cache
- no dependency on legacy `AI_space/` content

Private templates should live in end-user project repos, not here.
