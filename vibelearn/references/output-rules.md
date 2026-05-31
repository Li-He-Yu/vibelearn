# Output Rules

## Output Files

- `Notes`: one markdown file containing summary, outline, and key terms.
- `Test`: one markdown file containing exam-oriented questions only.
- `Ans`: one markdown file recording answers and source scope for each question.

## Naming

- Use the naming patterns defined in `vibelearn.config.yaml`.
- Default patterns:
  - `Notes -- Ch{chapter} {topic}.md`
  - `Test -- Ch{chapter} {topic}.md`
  - `Ans -- Ch{chapter} {topic}.md`
- For single-file input, preserve the original filename as the default topic unless the project config overrides it.
- For multi-file input, derive a combined topic from filenames and repeated concepts rather than picking one file arbitrarily.

## Project Overrides

- Project config may override the bundled note/test templates with private files outside the skill folder.
- Project config may point to project-owned guidance markdown when the default bundled templates are not sufficient.
- Treat these project overrides as the highest-priority source for subjective formatting and style.

## Placement

- Write outputs only to the configured `#Notes`, `#Test`, and `#Ans` folders.
- Keep generated study artifacts out of the skill folder itself.

## Scope Marking

- Every test question must include source scope.
- Every answer entry in `Ans` must point back to the same question number and source scope.
- Prefer page-based or section-based scope when the cache contains page separators or headings.
- If only a coarse scope is available, report the best available file and section instead of fabricating precision.

## Answer Key Rules

- `Ans` should be written as the canonical answer key, not as a second notes file.
- Each question needs a direct answer first; add key steps or scoring points only when the question type needs them.
- For calculation or derivation questions, include the essential steps needed to justify the result.
- For definition or short-answer questions, highlight the must-hit terms that determine correctness.

## Inline Interaction

- When grading, only evaluate a file after the user has written answers into it.
- If the user writes `?` or `不確定` inside the answer file, treat that as an inline question and answer it in place.
- Keep proactive advice inside a dedicated reminder block rather than mixing it into notes or question bodies.
