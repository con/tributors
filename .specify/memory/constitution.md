<!--
Sync Impact Report
==================
Version change: TEMPLATE → 1.0.0 (initial ratification)

Templates requiring updates:
  ✅ .specify/templates/plan-template.md — "Constitution Check" gate
     references this file generically; gate items are determined per-
     feature by /speckit.plan from the principles below. No edit required.
  ✅ .specify/templates/{spec,tasks,checklist}-template.md — no edits.
Top-level AI-agent guidance:
  ✅ AGENTS.md created at repository root as canonical guidance file.
  ✅ CLAUDE.md (locally excluded) symlinked → AGENTS.md.
Deferred TODOs: declare `black`/`pyflakes` as dev extras + wire into CI;
  the Quality Gates "Style" item promotes from operator-installed to a
  MUST gate at that point (next PATCH bump).
-->

# Tributors Constitution

Tributors pays tribute to every contributor by automating bookkeeping
across `all-contributors`, `Zenodo`, `CodeMeta`, `mailmap`, and
ORCID-backed identity. This constitution sets the non-negotiable rules
every change MUST follow.

## Core Principles

### I. Comprehensive Contributor Acknowledgement

Every person who has made a verifiable contribution to a downstream project
that exceeds the user-configured threshold MUST be representable in the
output formats Tributors supports. The default behaviour is *inclusive*: an
operator opts contributors *out* (via skip lists or a higher threshold), not
*in*. Bots are excluded by default because they are not people, not because
their work doesn't count.

**Rationale**: The whole purpose of the project is to make sure no
contributor falls through the cracks. A silent omission is a worse failure
than a noisy one.

### II. Named Contributor Fields Are Sacred (NON-NEGOTIABLE)

Once truthy, the named contributor fields — `name`, `email`, `affiliation`,
`orcid`, `blog`/`profile`, `bio` — in `.tributors`, `.zenodo.json`,
`.all-contributorsrc`, `codemeta.json`, and any future contributor file
MUST NOT be overwritten by an automated run. New information may be added;
existing values may not be silently replaced.

**Rationale**: operators hand-curate this exact set of fields; destroying
that work breaks trust. New parsers and update paths route through the
shared merge logic; unconditional assignment to a populated named field is
a violation that MUST be justified in Complexity Tracking or rejected.

**Known scope limit**: the codebase rebuilds container structures (e.g.,
`.all-contributorsrc` `contributors`, `.zenodo.json` `creators`) on each
run, so list *order* is not preserved. Order preservation is a SHOULD, not
a MUST, until a parser explicitly opts in.

### III. Pluggable Parsers & Shared Cache

Each input source and each output format MUST be implemented as a parser
deriving from `ParserBase` (`tributors/main/parsers/base.py`). Cross-parser
state MUST flow through the single shared cache file `.tributors`, indexed
by the canonical identity (the GitHub login when available; otherwise the
most stable identifier the parser exposes). Parsers MUST NOT reach across
into each other's file formats directly.

**Rationale**: The shared cache is what makes "update Zenodo from data the
all-contributors run discovered" cheap and consistent. Bypassing it
re-introduces the manual-bookkeeping problem the project was built to solve.

**How to apply**: A new format (e.g., a new author file standard) is added
by writing a parser, not by patching an existing one. A new identity source
updates `.tributors` via `update-lookup`; it does not write directly into a
contributor file.

### IV. Automation Across Equivalent Surfaces

Every contributor-management capability MUST be reachable from the Python
library API, the `tributors` CLI, the published container image, and the
GitHub Action (`action.yml`), with matching options (CLI dashes ↔ Action
underscores) and equivalent results. A feature is not "done" until the CLI
and (where applicable) the Action expose it, and its output is a
deterministic, diff-friendly file reviewable in a pull request.

### V. Identity Resolution with Human-in-the-Loop

When automatic identity resolution is ambiguous (e.g., multiple ORCID
records match a name), Tributors MUST NOT silently pick one. The default
behaviour is to skip the ambiguous entry; under `--interactive` mode, the
operator is prompted with each candidate's distinguishing fields and
selects (or skips). External authoritative sources (ORCID, mailmap, the
shared cache) take precedence over heuristic guesses.

**Rationale**: A wrong attribution is worse than a missing one — it
misrepresents a real person. Ambiguity is a signal that human judgement is
required, not that the tool should pick the first match.

## Metadata & Standards Compliance

Output files MUST conform to the upstream schemas they target:

- `.all-contributorsrc` follows the all-contributors specification, including
  the documented contribution-type emoji keys.
- `.zenodo.json` follows Zenodo's metadata schema; ORCID IDs are stored in
  their canonical format.
- `codemeta.json` follows the CodeMeta specification.
- `.mailmap` follows git's mailmap syntax.

Tributors MUST NOT invent new fields inside these files, MUST NOT reorder
or rewrite content beyond what is necessary to apply an update, and MUST
preserve any keys it does not understand so that hand-edits and
out-of-band tooling continue to work.

## Development Workflow & Quality Gates

The following gates apply to every change (human-authored or AI-assisted)
and MUST be checked by `/speckit.plan` for any new feature:

1. **Principle compliance**: every Functional Requirement in the spec is
   mapped to one or more principles above; any deviation appears in
   Complexity Tracking with explicit justification.
2. **Parser discipline**: new behaviour for an existing format goes into
   that format's parser; cross-format flow goes through `.tributors`.
3. **Surface parity**: behaviour added to the library is reflected in the
   CLI and (where applicable) the GitHub Action with matching options.
4. **Tests**: unit tests for parser logic (`tests/test_parsers.py` and
   peers) and CLI tests (`tests/test_client.sh`) MUST cover the new path;
   the merge-without-overwriting invariant MUST be exercised whenever a
   parser's write path is touched.
5. **Style**: Python source is formatted with `black` and passes
   `pyflakes`; both are operator-installed today and not yet wired into
   CI (the gate promotes to MUST when they are). New files MUST carry the
   MPL-2.0 license header in the form used across the codebase.
6. **No silent network calls in tests**: parser tests MUST be runnable
   offline; live API interaction goes behind an explicit fixture/flag.

## Governance

This constitution supersedes ad-hoc conventions in the codebase and other
guidance documents (including `AGENTS.md` / `CLAUDE.md`, README, and per-
parser docs). Where any of those conflict with this file, this file wins
and the conflicting document MUST be reconciled.

**Amendment procedure**: amendments are proposed in a pull request that
edits this file and, when applicable, the affected templates under
`.specify/templates/`. The PR description MUST include the version bump
(see below) and a Sync Impact Report at the top of this file describing
what changed and which downstream artifacts (templates, AGENTS.md,
parsers, docs) require follow-up. The PR MUST be reviewed by a project
maintainer before merge.

**Versioning policy**: the constitution itself uses semantic versioning.

- MAJOR: a principle is removed or redefined in a backward-incompatible way
  (e.g., relaxing the "manual edits are sacred" invariant).
- MINOR: a new principle or normative section is added, or existing
  guidance is materially expanded.
- PATCH: clarifications, wording fixes, typo repairs, non-semantic
  refinements.

**Compliance review**: every pull request that adds or modifies behaviour
MUST verify against the Quality Gates above. AI agents (Claude Code,
Codex, Cursor, Aider, and any future assistant) MUST read this
constitution and `AGENTS.md` before proposing changes, and MUST surface
principle violations rather than silently work around them.
`AGENTS.md` (and its `CLAUDE.md` symlink) is this constitution's delegate
for day-to-day conventions — build/test commands, code style specifics,
pointers back here. Principles are added here, not there.

**Version**: 1.0.0 | **Ratified**: 2026-05-18 | **Last Amended**: 2026-05-18
