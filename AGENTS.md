# AGENTS.md

Canonical guidance for AI coding agents (Claude Code, Codex, Cursor, Aider,
and any future assistant) and for humans who want a quick orientation.
`CLAUDE.md` in this directory is a symlink to this file.

## Read these first — every session

1. **`.specify/memory/constitution.md`** — the project's constitution. It
   defines the non-negotiable principles (most importantly: named
   contributor fields, once set, MUST NOT be overwritten — see principle
   II). Any change you propose MUST be consistent with it; surface a
   conflict rather than working around one.
2. **This file** — for build/test commands and code-style conventions.
3. The plan for the current feature, if one is active under `specs/`.

## Spec-Kit Workflow

This project uses [spec-kit](https://github.com/github/spec-kit) for
feature work. The relevant slash commands and the artifacts they
produce/consume:

| Command                 | Reads                     | Writes                                          |
| ----------------------- | ------------------------- | ----------------------------------------------- |
| `/speckit.constitution` | repo context              | `.specify/memory/constitution.md`               |
| `/speckit.specify`      | constitution              | `specs/<###-name>/spec.md`                      |
| `/speckit.clarify`      | spec                      | spec (updated)                                  |
| `/speckit.plan`         | spec, constitution        | `plan.md`, Phase 0/1 artifacts, agent context   |
| `/speckit.tasks`        | plan + Phase 1 artifacts  | `tasks.md`                                      |
| `/speckit.implement`    | tasks, plan, constitution | source / tests                                  |

Each command is bounded — do not silently progress into the next one.

## Build and Test Commands

- Install: `pip install .[all]` (`pytest` is not pulled in by `[all]`; add
  it explicitly for the test suite, e.g. `pip install -e .[all] pytest`)
- Run tests: `pytest -sv tests/*.py`
- Run CLI tests: `/bin/bash tests/test_client.sh`
- Run a single test: `pytest -sv tests/test_parsers.py::test_parser_zenodo`
- Format code: `black tributors`
- Check formatting: `black --check tributors`
- Check imports: `pyflakes tributors`

Parser tests MUST be runnable offline; do not introduce live network
calls without an explicit opt-in fixture/flag.

## Code Style Guidelines

### Python

- Format with Black; follow PEP 8 for everything Black does not enforce.
- Public classes and functions get a docstring (`"""triple quotes"""`).
- Import order: standard library, then third-party, then local — separated
  by blank lines. Use relative imports within the `tributors` package.
- `snake_case` for variables and functions; `PascalCase` for classes.
- Catch specific exceptions, not bare `except:`.
- New `.py` files MUST start with the MPL-2.0 header used across the
  codebase (see `tributors/main/parsers/base.py` for the canonical form).

### Markdown

- Markdown tables MUST be column-aligned in source: every cell padded to
  the column's widest content, separator dashes matching, outer pipes
  vertical. The raw `.md` is read as often as the rendered view.

## Architecture in One Paragraph

`tributors` is a Python library + CLI + container + GitHub Action. Each
input source or output format is a *parser* deriving from `ParserBase`
(`tributors/main/parsers/base.py`). Parsers exchange information through a
single shared cache file, `.tributors`, indexed by GitHub login when
available. `update-lookup` populates the cache from sources (GitHub API,
mailmap, ORCID, etc.); `update` writes from the cache into per-format
files (`.all-contributorsrc`, `.zenodo.json`, `codemeta.json`, …) without
overwriting populated fields. New formats are added by writing new
parsers, not by patching existing ones — see the constitution, principle
III, for the rationale.

## What Counts as "Done"

See `.specify/memory/constitution.md` § "Development Workflow & Quality
Gates" for the authoritative checklist. Short form: parser/cache
discipline (III), surface parity (IV), tests covering the no-overwrite
invariant (II), `black` + `pyflakes` clean, deterministic diff-friendly
output.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
under `specs/<active-feature>/plan.md`.
<!-- SPECKIT END -->
