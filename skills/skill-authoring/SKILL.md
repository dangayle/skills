---
name: skill-authoring
description: Create, edit, rename, review, or publish an Agent Skill in Dan's skills repository (github.com/dangayle/skills). Use whenever the user asks to create a new skill, capture a workflow or checklist as a skill, update or restructure a SKILL.md, or push skills to GitHub.
license: Apache-2.0
metadata:
  repository: https://github.com/dangayle/skills
---

# Skill authoring

Every skill Dan owns lives in one repository, following the [Agent Skills specification](https://agentskills.io/specification):

- Local clone: `C:\Users\dangayle\src\skills`
- Remote: <https://github.com/dangayle/skills>

`AGENTS.md` at the repository root is the authoritative style guide. Read it before editing. This skill is the workflow around it.

## Workflow

1. **Check for overlap first.** List `skills/` and read the table in `README.md`. If an existing skill covers the request, extend it instead of adding a near-duplicate.
2. **Create the file** at `skills/<skill-name>/SKILL.md`. The directory name must equal the frontmatter `name`; validation enforces this.
3. **Write routing-first frontmatter:**

   ```yaml
   ---
   name: <skill-name>
   description: <what it does>. Use when <triggers: symptoms, task types, phrases the user would actually say>.
   license: Apache-2.0
   ---
   ```

   - `name`: lowercase letters, digits, single hyphens, 1–64 characters.
   - `description`: 1–1024 characters. It is the only text an agent sees before deciding to load the skill, so lead with the verbs and keywords a real request would contain. Do not bury the trigger at the end of a long summary.
   - Optional: `compatibility` (≤500 chars, only genuine environment requirements), `metadata` (string→string map), `allowed-tools` (experimental). Any other field fails validation.
4. **Write the body for an agent with no prior context.** Order it as: when to use / when not to, then the procedure, then failure modes. Imperative voice, concrete commands, no marketing prose.
5. **Push detail down.** Keep `SKILL.md` under ~500 lines. Long tables, API surfaces, and edge cases go in `references/*.md` and are linked with relative paths so they load only when needed. Executables go in `scripts/`, templates in `assets/`.
6. **Validate:**

   ```sh
   python scripts/validate.py        # install once: pip install skills-ref
   ```

7. **Document it:** add a row to the skills table in `README.md`.
8. **Install it locally** so Pi can use it. Prefer a junction (live edits, no copy drift):

   ```sh
   powershell -NoProfile -Command "New-Item -ItemType Junction -Path \"$HOME\.pi\agent\skills\<skill-name>\" -Target \"C:\Users\dangayle\src\skills\skills\<skill-name>\""
   ```

   Then `/reload` in an active session. On another machine, `npx skills add dangayle/skills --skill <skill-name>` is the portable route.
9. **Commit and push:**

   ```sh
   git add -A
   git commit -m "feat(<skill-name>): <summary>"
   git push
   ```

   Use `fix(<skill-name>):` for corrections and `docs:` for repository-wide edits.

## Quality bar

- No secrets, tokens, absolute machine paths outside this repository, or personal data.
- No binaries, generated output, or files over 512 KB.
- Scripts are non-interactive, deterministic, and document usage in a header comment.
- A rename means directory, `name`, README row, and local junction all change together.
- If the skill would be useful to anyone but Dan, it still belongs here — write it generically and keep Dan-specific context in `metadata` or a short "Context" section.
