# Agent Skills

A collection of [Agent Skills](https://agentskills.io) — portable, version-controlled folders of instructions that AI coding agents load on demand.

Each skill follows the [Agent Skills specification](https://agentskills.io/specification): a directory containing a `SKILL.md` file with YAML frontmatter (`name`, `description`) plus any supporting references, scripts, or assets.

## Skills

<!-- Keep this table in sync when adding or renaming a skill. -->

| Skill | Description |
| ----- | ----------- |
| [skill-authoring](skills/skill-authoring/SKILL.md) | Create, edit, validate, and publish skills in this repository. |
| [dual-projection-sync](skills/dual-projection-sync/SKILL.md) | Keep specification, implementation, and tests synchronized as three co-equal projections of one contract; reconstruct any missing projection. |

## Install

### `npx skills`

Install every skill in this repository into your agent's skills directory:

```sh
npx skills add dangayle/skills
```

### Install a single skill

```sh
npx skills add dangayle/skills --skill <skill-name>
```

### Clone and copy

```sh
git clone https://github.com/dangayle/skills.git
cp -r skills/<skill-name> ~/.claude/skills/
```

| Agent         | Skill directory      |
| ------------- | -------------------- |
| Claude Code   | `~/.claude/skills/`  |
| Codex         | `~/.codex/skills/`   |
| Cursor        | `~/.cursor/skills/`  |
| OpenCode      | `~/.config/opencode/skills/` |
| Pi            | `~/.pi/agent/skills/` |

## Repository layout

```
skills/
└── <skill-name>/
    ├── SKILL.md      # Required: frontmatter + instructions
    ├── references/   # Optional: detailed docs loaded on demand
    ├── scripts/      # Optional: executable helpers
    └── assets/       # Optional: templates and static files
```

A skill directory name must exactly match the `name` field in its `SKILL.md`.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter:

   ```markdown
   ---
   name: skill-name
   description: What it does and when to use it. Include the keywords an agent would match on.
   license: Apache-2.0
   ---
   ```

2. Write the instructions. Keep `SKILL.md` focused and under ~500 lines; move long detail into `references/` and link to it.
3. Validate:

   ```sh
   python scripts/validate.py
   ```

4. Add the skill to the table above and open a pull request.

See [AGENTS.md](AGENTS.md) for authoring conventions and [the specification](https://agentskills.io/specification) for the format rules.

## Validate

```sh
pip install skills-ref   # or: uvx --from skills-ref skills-ref validate skills/<name>
python scripts/validate.py
```

CI runs the same script on every push and pull request.

## License

[Apache License 2.0](LICENSE). Individual skills may carry their own `license` field.
