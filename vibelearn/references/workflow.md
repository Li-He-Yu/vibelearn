# Workflow

## Workflow Branches

- Default branch: generate notes, test, and answer key in one run.
- Narrow branch: generate only the artifact family the user explicitly asks for.
- Grading branch: grade an answered markdown file without regenerating questions.

The user does not need to write an explicit `MODE = ...` line. Infer the branch from the request, and default to the all-in-one path when the request is broad.

## Startup Order

1. If the user asks to initialize project config, run `vibelearn/scripts/init_project_config.py`.
2. Read `./vibelearn.config.yaml`.
3. Read `vibelearn/config/skill.defaults.yaml`.
4. Resolve preference files, then merge project-level overrides:
   - optional template overrides from `vibelearn.config.yaml`
   - optional guidance files from `vibelearn.config.yaml`
   - built-in defaults from `vibelearn/config/skill.defaults.yaml` when the project does not override them
5. Load only the reference files needed for the current branch.

## Generation Order

1. Identify single-file or multi-file input.
2. Check `vlcache/manifests/` and the configured cache directories first.
3. Prefer the richest available cache format for the source:
   - project-provided markdown cache when available
   - otherwise the canonical text cache from `vlcache/pdf_text/`
4. If cache is missing or stale and the source is a PDF, run the configured extraction script.
5. In the default branch, generate notes first, then test, then answer key.
6. In a narrower branch, generate only the requested artifact family.
7. Generate test and answer key from the source material and notes, but do not mechanically expand every note bullet into a question.
8. For grading, operate on the answered markdown file directly and answer inline questions where present.

## Project Overrides

- `templates.*`: optional project-owned template paths. Use these before the bundled defaults when present.
- `guidance.*`: optional project-owned markdown references for subjective style decisions such as note density, preferred question mix, or answer-key detail.
- `generation.*`: high-level hints for density, strictness, and answer-detail preferences when no stronger project guidance file is provided.

## Source Lookup

If the user asks where a concept or a question came from:

1. Search the cache first, starting from the manifest and the cached text or markdown.
2. Use page separators, headings, or cached scope markers to narrow the source.
3. If the relevant passage is not in cache, go back to the original source file.
4. Report the best available file and scope reference rather than inventing a citation.
