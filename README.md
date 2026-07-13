# Cortex Skills Team Repository

This repository is a shared place for the team to upload, review, and reuse Cortex Code skills in CoCo.

The pattern is simple:

1. A team member creates a skill folder under `skills/`.
2. The skill includes a `SKILL.md` file and any supporting references.
3. Other team members install or sync this repo in CoCo.
4. Everyone can invoke shared skills with `$skill-name`.

## How To Use These Skills In CoCo

Install the full repo in CoCo:

```text
Install the skills from https://github.com/<org>/<repo>
```

For local testing before the repo is pushed:

```text
Install the skills from C:\Users\Yash.Malviya\OneDrive - Commonwealth of Massachusetts\Desktop\COMO COCO\CORTEX_SKILLS
```

After someone adds or updates a skill:

```text
Sync my skills
```

List installed skills:

```text
/skill list
```

Use a skill:

```text
$commonwealth-data-review Help me review this dataset workflow before I share it with another team.
```

Install one skill instead of the whole repo:

```text
Install the skill at https://github.com/<org>/<repo>/tree/main/skills/<skill-name>
```

More detailed usage notes are in [docs/coco-usage.md](docs/coco-usage.md).

## How The Repo Is Organized

```text
skills/
  _template/
    SKILL.md
    LICENSE
    references/
    scripts/
    assets/
  commonwealth-data-review/
    SKILL.md
    LICENSE
    references/
```

Every real skill should live at:

```text
skills/<skill-name>/
```

The folder name and the `id` field in `SKILL.md` should match.

## Current Skills

| Skill | Status | Purpose |
| --- | --- | --- |
| [`commonwealth-data-review`](skills/commonwealth-data-review) | draft | Example shared skill for reviewing datasets or analysis workflows before handoff. |
| [`_template`](skills/_template) | template | Copy this folder when creating a new skill. |

## Add A New Skill

1. Copy `skills/_template/`.
2. Rename the copied folder to your skill name, using lowercase letters and hyphens.
3. Edit `SKILL.md`.
4. Add any supporting docs under `references/`.
5. Test it in CoCo.
6. Open a pull request or upload the folder to GitHub.
7. Ask the team to run `Sync my skills` in CoCo.

The team process is documented in [docs/team-process.md](docs/team-process.md).

## Basic Rules

- Do not upload secrets, passwords, tokens, private keys, or connection strings.
- Do not upload protected data or production extracts.
- Keep each skill focused on one reusable workflow.
- Put long examples or checklists in `references/`.
- Use `draft`, `beta`, `stable`, or `archived` for status.
- Test the skill with the example prompt before sharing it.

## Validate Skills

Run this locally before sharing changes:

```powershell
python .github/scripts/validate_skill.py --all
```

