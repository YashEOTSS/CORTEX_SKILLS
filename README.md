# Cortex Skills Team Repository

This repository is a shared place for the team to upload, review, and reuse Cortex Code skills in CoCo.

The pattern is simple:

1. A team member creates a skill folder under `skills/`.
2. The skill includes a `SKILL.md` file and any supporting references.
3. Other team members install or sync this repo in CoCo.
4. Everyone can invoke shared skills with `$skill-name`.

## How To Use These Skills In CoCo Desktop

### Install the full repo as a plugin

In the CoCo Desktop chat, type:

```text
I have a github which has skills in it I want to use in cortex code: https://github.com/YashEOTSS/CORTEX_SKILLS.git
```

CoCo will clone the repo, create a plugin manifest, and register it automatically. The plugin appears in **Agent Settings > Plugins** within a few seconds.

### Install a single skill from the repo

```text
Install the skill at https://github.com/YashEOTSS/CORTEX_SKILLS/tree/main/skills/commonwealth-data-review
```

### Sync after updates

When someone pushes changes to the repo, click the **Sync** button on the plugin's detail page in Agent Settings, or type:

```text
Sync my skills
```

### Use a skill

Invoke a skill by name with the plugin prefix:

```text
$cortex-skills:commonwealth-data-review Help me review this dataset workflow before I share it with another team.
```

```text
$cortex-skills:data-ingest-medallion Ingest my CSV into Snowflake.
```

### For local testing (before pushing to GitHub)

If you want to test skills from a local folder instead of GitHub, use the local plugin installer:

```text
/local-plugin-installer C:\path\to\your\local\CORTEX_SKILLS
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

