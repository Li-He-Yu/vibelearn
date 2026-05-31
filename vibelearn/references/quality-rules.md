# Quality Rules

This file defines output quality for `Notes`, `Test`, `Ans`, and `Grading`.
Template selection belongs to `vibelearn/assets/ASSETS.md`; this file governs what the final content should be like after a template is chosen.

If the project config provides guidance files or generation hints, apply them before falling back to the built-in defaults below.

## Notes

- Focus on exam-relevant structure, terminology, and mechanisms.
- Keep the outline aligned with likely teaching or exam order.
- Select key terms that are central, testable, or prerequisites for later topics.
- When the source is introductory or narrow, keep the note set proportionate instead of inflating coverage.
- Short examples are acceptable when they clarify a mechanism or term, but avoid turning notes into a tutorial.
- Match the configured note-density hint unless a project guidance file gives more specific instructions.

## Test Design

- Mix question types when the material supports it.
- Keep numbering continuous.
- Mark source scope for every question.
- Scale question count to topic density instead of forcing a fixed pattern.
- Merge repeated concepts across multi-file inputs rather than asking the same idea several times.
- Do not overfit to incidental examples or slide-local trivia unless they represent a real core concept.
- Match the configured test-density hint unless a project guidance file gives more specific instructions.

## Answer Key

- Keep the answer key aligned one-to-one with the final question numbering.
- Start with the direct answer before adding explanation.
- Include essential reasoning or scoring points for questions where correctness depends on steps, terminology, or structure.
- Do not let the answer key drift into long-form teaching notes unless clarification is required for grading quality.
- Match the configured answer-detail hint unless a project guidance file gives more specific instructions.

## Grading

- Use exam-style strictness.
- Definition questions require the core definition.
- Computation questions require correct steps or correct result depending on the question type.
- Essay answers that are directionally correct but missing required terminology should be marked incomplete or incorrect with explanation.
- Explain mistakes, not already-correct parts.
- When the user leaves `?` or `不確定` in the answer file, respond to that uncertainty directly in the grading output.
- Match the configured grading strictness hint unless a project guidance file gives more specific instructions.
