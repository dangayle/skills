# Agent Instructions

This repository is a collection of [Agent Skills](https://agentskills.io) for Dan Gayle. The format is defined by the [Agent Skills specification](https://agentskills.io/specification); that specification, not existing skills here, is authoritative.

## Layout

- One skill per directory: `skills/<skill-name>/SKILL.md`.
- `<skill-name>` must match the `name` field in the frontmatter exactly, use lowercase letters, digits, and single hyphens, and stay within 64 characters.
- Optional supporting directories: `references/` (progressive-disclosure docs), `scripts/` (executable helpers), `assets/` (templates and static files). Any other files are allowed but keep the skill lean.
- Never add generated output, dependency trees, secrets, binaries, or files over 512 KB. Keep each skill under 2 MB.

## Frontmatter

Required:

- `name` — lowercase, hyphenated, matches the directory.
- `description` — 1–1024 characters. Say **what** the skill does and **when** to use it, in the words a user or agent would actually use. This is the only text an agent sees before deciding to load the skill.

Optional: `license`, `compatibility` (≤500 chars, only for real environment requirements), `metadata` (string→string map), `allowed-tools` (experimental; space-separated). No other fields are allowed.

## Writing a skill

- Write imperative instructions addressed to the agent, not prose about the skill.
- Put the decision-making first: when to use it, when not to, and the order of operations.
- Use progressive disclosure. Keep `SKILL.md` under ~500 lines and outcome-focused; move long tables, API detail, and edge cases into `references/*.md` and link them with relative paths.
- Prefer retrieval over memory for versioned or fast-moving APIs: link the canonical docs and tell the agent to read them.
- Scripts must be non-interactive, deterministic, dependency-light, and document usage in a header comment. Reference them by paths relative to the skill directory.
- No secrets, tokens, machine-specific absolute paths, or personal data.

## Changing a skill

- A rename means renaming the directory and the `name` field together, then updating `README.md`.
- Keep diffs scoped to one skill unless the change is repository-wide.
- Update the skill table in `README.md` when adding or removing a skill.

## Validate

Run before committing:

```sh
python scripts/validate.py
```

Install the reference validator first if needed: `pip install skills-ref`. CI (`.github/workflows/validate.yml`) runs the same script.
