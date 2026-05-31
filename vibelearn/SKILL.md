---
name: vibelearn
description: Generate exam-oriented notes, tests, answer keys, and grading feedback from course materials such as PDFs or cached extracted text. Use when the repo contains `vibelearn/` plus a root `vibelearn.config.yaml` describing outputs, cache, and material paths.
---

# Vibe Learn

Use this skill when the user wants to turn course materials into:

- `Notes`: summary, outline, and key terms
- `Test`: exam-oriented questions
- `Ans`: answer key with source scope
- `Grading`: grading and feedback for a completed test file

This skill is workflow-oriented. Keep project-specific paths and output decisions in `./vibelearn.config.yaml`. Keep reusable skill-internal paths and templates in `vibelearn/config/skill.defaults.yaml`. Do not hardcode repo-specific paths in ad hoc prompts when the config files already define them.

## Core Rules

- Do not modify or delete original course materials such as PDFs.
- Write generated outputs to the configured output folders only.
- Prefer cached extracted text before re-reading a PDF.
- Treat `vlcache/` as runtime state owned by the project, not by the skill bundle itself.
- Keep outputs exam-oriented, concise in tone, and structurally stable.
- Treat a small source file as a small concept unit; do not inflate it into a full chapter.
- If the source is ambiguous or incomplete, state that explicitly instead of guessing.
- Prefer neutral phrasing such as `current course materials` unless the source clearly establishes a more specific course identity.

## Startup

1. If the user asks to initialize or bootstrap config, run `vibelearn/scripts/init_project_config.py`.
2. Read `./vibelearn.config.yaml`.
3. Read `vibelearn/config/skill.defaults.yaml`.
4. Read the preference files defined by the skill defaults, then apply any project-level guidance files configured in `vibelearn.config.yaml`.
5. If needed, read:
   - `vibelearn/references/workflow.md` for execution flow
   - `vibelearn/references/output-rules.md` for filename, scope, and inline interaction rules
   - `vibelearn/references/quality-rules.md` for note, test, answer-key, and grading quality rules
   - `vibelearn/assets/ASSETS.md` for template selection
6. Infer the requested workflow branch from the user request:
   - default to generating `Notes`, `Test`, and `Ans` together
   - generate only one branch when the user explicitly asks for that narrower scope
   - use grading-only flow when the user provides an answered file to review

## Execution Flow

### Notes / Test generation

1. Resolve whether the input is a single file or a multi-file chapter unit.
2. Check `vlcache/` using the configured cache paths first.
3. If cache is missing or stale and the source is a PDF, use the configured extraction script.
4. Select the matching template from the configured template paths.
   - Use project-level template overrides from `vibelearn.config.yaml` first when they are present.
   - Fall back to the bundled template paths from `vibelearn/config/skill.defaults.yaml` otherwise.
5. By default, generate `Notes`, then `Test`, then `Ans` in one pass unless the user asked for a narrower branch.

### Grading

1. Grade only after the user has written answers into a target markdown file.
2. If the answer file contains `?` or `不確定`, treat that as a request for explanation and respond inline.
3. Use exam-style strictness:
   - missing core term in a definition question counts as incorrect
   - wrong computation step or result counts as incorrect
   - essay answers with the right direction but missing essential terminology should be marked incomplete and explained
4. Prefer editing the answer file directly or use the configured grading script when deterministic writeback helps.

## Output Expectations

- Default output language is Traditional Chinese with necessary English terminology.
- Preserve technical terms in English where appropriate.
- For abbreviations used in the source material, include the full name in the key terms section.
- Avoid flattery, filler, and broad pedagogical digressions.
- Apply the configured naming patterns for `Notes`, `Test`, and `Ans`.
- Respect project-level density and answer-detail hints before falling back to the built-in defaults.
- Include source scope for each test question.
- Keep proactive suggestions inside a clearly separated reminder section rather than inside notes or question bodies.

## File Roles

- `vibelearn.config.yaml`
  Project-specific paths, cache layout, output folders, naming rules, optional template overrides, and optional style-guidance files.
- `vibelearn/config/`
  Reusable skill defaults and language/content preferences.
- `vibelearn/references/`
  Detailed workflow and quality rules. Read only as needed.
- `vibelearn/assets/`
  Output templates and examples.
- `vibelearn/scripts/`
  Deterministic helper scripts.
- `vlcache/`
  Runtime cache for extracted text, optional markdown conversions, and manifests.

## Boundaries

- Do not paste full generated notes, tests, or grading logs back into `SKILL.md` or config files.
- Do not treat cached text as immutable truth when the user indicates the PDF changed.
- Do not mechanically mirror every bullet from the notes into test questions.

## Maintainer

- Maintainer: Li-He-Yu
- Preserve the bundled `LICENSE.txt` and `NOTICE.txt` when redistributing or modifying this skill bundle.
