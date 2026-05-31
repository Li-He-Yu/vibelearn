# VibeLearn

VibeLearn is a Codex skill for turning course materials into exam-oriented notes, tests, answer keys, and grading feedback.

This repository is the public source repo for the `vibelearn` skill bundle. It intentionally excludes private course PDFs, personal outputs, and runtime cache.

## Maintainer

- Author / Maintainer: Li-He-Yu
- License direction: Apache License 2.0 with NOTICE-based attribution

## Repository Layout

```text
.
|-- vibelearn/     # skill bundle
|-- docs/          # repo-level design notes
|-- examples/      # sample project config and style guidance
|-- LICENSE
`-- README.md
```

## Install the Skill

Copy `vibelearn/` into your local Codex skills directory:

- Windows: `%USERPROFILE%\\.codex\\skills\\vibelearn`
- macOS/Linux: `~/.codex/skills/vibelearn`

After copying, restart Codex.

Once this repo is published, you can also install from the GitHub path with `$skill-installer`.

## Initialize a Project

In the target course-material repo:

1. Ask Codex: `$vibelearn initialize config for this repo`
2. Or run the bootstrap script directly:

```powershell
python path\\to\\vibelearn\\scripts\\init_project_config.py .
```

This creates `vibelearn.config.yaml` in the project root.

## Customize Behavior

Edit `vibelearn.config.yaml` to control:

- output directories
- cache directories
- naming patterns
- generation density and grading strictness hints
- optional template overrides
- optional guidance markdown files

If you do not want to publish your private templates, keep them outside the skill bundle and point `templates.*` to project-owned files.

If you want style control without shipping templates, start from:

- `examples/style-guidance.md`
- `vibelearn/assets/example-style-guidance.md`

Then point `guidance.*` entries in `vibelearn.config.yaml` to your project-owned guidance files.

## Validate Changes

Quick validation:

```powershell
python -X utf8 <path-to-your-codex-home>\skills\.system\skill-creator\scripts\quick_validate.py vibelearn
```

Script syntax check:

```powershell
Get-ChildItem vibelearn\scripts\*.py | ForEach-Object { python -m py_compile $_.FullName }
```

## Examples

- `examples/vibelearn.config.yaml`: public sample project config
- `examples/style-guidance.md`: placeholder for private note/test/answer/grading preferences

Sample input and output artifacts are intentionally not bundled yet.

## License

This repository and the bundled skill are released under the Apache License 2.0.

- Root license text: [LICENSE](LICENSE)
- Root attribution notice: [NOTICE](NOTICE)
- Skill-bundle notice: [vibelearn/NOTICE.txt](vibelearn/NOTICE.txt)
