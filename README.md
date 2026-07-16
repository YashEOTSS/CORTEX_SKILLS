# Cortex Skills Team Repository

A shared repository for the ODIA team to create, review, and reuse Cortex Code (CoCo) skills. Team members contribute skills as pull requests, and everyone syncs the repo into CoCo Desktop to use them.

---

## How It Works (Quick Visual)

### Creating and Sharing a Skill

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SKILL AUTHOR WORKFLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  1. COPY     │     │  2. EDIT     │     │  3. VALIDATE │
  │  _template/  │────▶│  SKILL.md    │────▶│  locally     │
  │              │     │  + LICENSE   │     │              │
  └──────────────┘     └──────────────┘     └──────┬───────┘
                                                   │
                                                   ▼
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  6. TEAM     │     │  5. MERGE    │     │  4. OPEN     │
  │  SYNCS in    │◀────│  to main     │◀────│  Pull        │
  │  CoCo        │     │  (CI passes) │     │  Request     │
  └──────────────┘     └──────────────┘     └──────────────┘
```

### Installing and Using Skills in CoCo Desktop

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       TEAM MEMBER WORKFLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────┐
  │  FIRST TIME ONLY                      │
  │                                       │
  │  In CoCo Desktop chat, type:          │
  │  "I have a github which has skills    │
  │   in it I want to use in cortex       │
  │   code: https://github.com/           │
  │   YashEOTSS/CORTEX_SKILLS.git"       │
  │                                       │
  │  ✓ Plugin installs automatically      │
  │  ✓ Appears in Agent Settings          │
  └───────────────────┬───────────────────┘
                      │
                      ▼
  ┌───────────────────────────────────────┐
  │  WHEN SKILLS ARE UPDATED              │
  │                                       │
  │  Click "Sync" in Agent Settings       │
  │  — or type: "Sync my skills"          │
  └───────────────────┬───────────────────┘
                      │
                      ▼
  ┌───────────────────────────────────────┐
  │  USE A SKILL                          │
  │                                       │
  │  $cortex-skills:skill-name <prompt>   │
  │                                       │
  │  Examples:                            │
  │  $cortex-skills:commonwealth-data-    │
  │    review Review my dataset.          │
  │  $cortex-skills:data-ingest-          │
  │    medallion Ingest my CSV.           │
  └───────────────────────────────────────┘
```

### End-to-End Flow

```
┌────────┐   push    ┌────────┐  CI validates  ┌────────┐   sync    ┌────────┐
│ Author │─────────▶ │ GitHub │ ─────────────▶  │  main  │ ────────▶│  CoCo  │
│ writes │           │   PR   │                 │ branch │           │Desktop │
│ skill  │           │        │  ◀── fix if     │        │           │(team)  │
└────────┘           └────────┘     failing     └────────┘           └────────┘
                                                                         │
                                                                         ▼
                                                                    ┌────────┐
                                                                    │ Team   │
                                                                    │ uses   │
                                                                    │ skill  │
                                                                    └────────┘
```

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Skill Format and Requirements](#skill-format-and-requirements)
- [Validation](#validation)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Installing Skills Into CoCo Desktop](#installing-skills-into-coco-desktop)
- [Using Skills Within the Team](#using-skills-within-the-team)
- [Adding a New Skill](#adding-a-new-skill)
- [Current Skills](#current-skills)
- [Rules](#rules)

---

## Repository Structure

```text
CORTEX_SKILLS/
├── .cortex-plugin/
│   └── plugin.json              # CoCo Desktop plugin manifest (required for install)
├── .github/
│   ├── scripts/
│   │   └── validate_skill.py    # Local and CI validation script
│   ├── workflows/
│   │   └── validate-skill.yml   # GitHub Actions workflow (runs on PR and push)
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── coco-usage.md            # Detailed CoCo usage guide
│   └── team-process.md          # Team roles and contribution process
├── skills/
│   ├── _template/               # Starter template — copy this for new skills
│   │   ├── SKILL.md
│   │   ├── LICENSE
│   │   ├── references/
│   │   ├── scripts/
│   │   └── assets/
│   ├── commonwealth-data-review/
│   │   ├── SKILL.md
│   │   ├── LICENSE
│   │   └── references/
│   │       └── review-checklist.md
│   └── data-ingest-medallion/
│       ├── SKILL.md
│       └── LICENSE
├── CONTRIBUTING.md
└── README.md
```

### Key Components

| Component | Purpose |
| --- | --- |
| `.cortex-plugin/plugin.json` | Plugin manifest so CoCo Desktop recognizes this repo as a plugin |
| `skills/<name>/SKILL.md` | The skill definition — frontmatter + instructions |
| `skills/<name>/LICENSE` | Required license file per skill |
| `skills/<name>/references/` | Supporting docs, checklists, examples referenced by the skill |
| `skills/_template/` | Copy this folder to start a new skill |
| `.github/scripts/validate_skill.py` | Validates skill format locally and in CI |
| `docs/` | Team process documentation and CoCo usage guide |

---

## Skill Format and Requirements

Every skill lives in its own folder at `skills/<skill-name>/` and must contain at minimum:

1. **`SKILL.md`** — the skill definition
2. **`LICENSE`** — must contain an approved license marker (`apache license`, `commonwealth`, `odia`, or `mit license`)

### SKILL.md Frontmatter

The `SKILL.md` file must start with YAML frontmatter delimited by `---`. All of the following fields are **required** for validation to pass:

```yaml
---
id: my-skill-name
name: my-skill-name
title: My Skill Title
summary: One sentence describing what this skill helps users do.
description: |
  Use when a user needs help with the specific workflow this skill supports.
  Include trigger terms and adjacent cases this skill should not handle.
authors: ODIA Team
status: draft
categories:
  - analytics
  - data-quality
tools:
  - Read
  - Grep
  - Bash
prompt: An example prompt that should activate the skill.
language: en
---
```

### Field Rules

| Field | Requirements |
| --- | --- |
| `id` | Lowercase letters, numbers, and hyphens only. Must match the folder name exactly. Pattern: `[a-z0-9]+(?:-[a-z0-9]+)*` |
| `name` | Should match `id` unless there is a clear reason to differ |
| `title` | Human-readable title for the skill |
| `summary` | One-sentence description |
| `description` | Multi-line description including trigger phrases and exclusions. This controls when CoCo auto-activates the skill |
| `authors` | Who created the skill |
| `status` | One of: `draft`, `beta`, `stable`, `archived` |
| `categories` | List of category tags |
| `tools` | List of CoCo tools the skill uses (e.g., `Read`, `Grep`, `Bash`) |
| `prompt` | An example prompt a user would type to trigger this skill |
| `language` | Language code (e.g., `en`) |

### SKILL.md Body Structure

After the frontmatter, include these sections:

```markdown
# Skill Title

## Overview
What this skill does and who it is for.

## When To Use
Bullet list of situations where this skill applies.

## When Not To Use
Bullet list of situations where this skill should NOT be used.

## Workflow
Numbered steps the skill follows.

## References
Links to files in the references/ folder.

## Stopping Points
Actions that require human confirmation before proceeding.

## Common Mistakes
Pitfalls to avoid when using this skill.
```

---

## Validation

The validation script checks every skill folder for correctness. It runs with zero external dependencies (pure Python 3 standard library).

### Run Locally

```powershell
python .github/scripts/validate_skill.py --all
```

Or validate a single skill:

```powershell
python .github/scripts/validate_skill.py skills/commonwealth-data-review
```

### What It Checks

| Check | What Happens If It Fails |
| --- | --- |
| `SKILL.md` exists | ERROR |
| Frontmatter starts and ends with `---` | ERROR |
| All 10 required fields are present and non-empty | ERROR per missing field |
| `id` matches the folder name | ERROR |
| `id` uses valid format (`[a-z0-9]+(?:-[a-z0-9]+)*`) | ERROR |
| `status` is one of `draft`, `beta`, `stable`, `archived` | ERROR |
| `LICENSE` file exists | ERROR |
| `LICENSE` contains an approved marker | ERROR |
| Files contain secret-like patterns (`password:`, `api_key:`, private keys, etc.) | WARNING |
| `name` differs from `id` | WARNING |

### Tips for Passing Validation Quickly

- Copy `skills/_template/` and fill in every field before running.
- Make sure `id` and the folder name are identical.
- Use only lowercase, numbers, and hyphens in your folder and `id`.
- Include a `LICENSE` file with "Apache License" or "MIT License" text.
- Do not leave placeholder text like `replace-with-skill-id` in the frontmatter.
- Avoid putting passwords, tokens, or API keys anywhere in the skill folder.

---

## GitHub Actions Workflow

The `validate-skill.yml` workflow runs automatically on:

- **Pull requests** that modify anything under `skills/`, the validation script, or the workflow file itself.
- **Pushes to `main`** that touch the same paths.

It runs `python .github/scripts/validate_skill.py --all` and fails the check if any skill has errors. This ensures no broken skill reaches `main`.

---

## Installing Skills Into CoCo Desktop

### Install the Full Repo (Recommended)

In the CoCo Desktop chat, type:

```text
I have a github which has skills in it I want to use in cortex code: https://github.com/YashEOTSS/CORTEX_SKILLS.git
```

CoCo will:
1. Clone the repository.
2. Create a plugin manifest if needed.
3. Register it in `~/.snowflake/cortex/plugins/cortex-skills/`.
4. The plugin appears in **Agent Settings > Plugins** within seconds.

### Install a Single Skill

```text
Install the skill at https://github.com/YashEOTSS/CORTEX_SKILLS/tree/main/skills/commonwealth-data-review
```

### Sync After Updates

When someone pushes changes to the repo, click the **Sync** button on the plugin's detail page in Agent Settings, or type:

```text
Sync my skills
```

### Local Testing (Before Pushing to GitHub)

To test from a local folder:

```text
/local-plugin-installer C:\path\to\your\local\CORTEX_SKILLS
```

### Verify Installation

After installing, confirm your skills are available:

```text
/skill list
```

---

## Using Skills Within the Team

### Invoke a Skill

Use the plugin prefix and skill name:

```text
$cortex-skills:commonwealth-data-review Help me review this dataset workflow before I share it with another team.
```

```text
$cortex-skills:data-ingest-medallion Ingest my CSV into Snowflake.
```

### Team Workflow

1. **Author** creates a skill folder and opens a pull request.
2. **Reviewer** checks clarity, safety, and usefulness. CI validation must pass.
3. **Merge** to `main`.
4. **Author** notifies the team (e.g., in Slack or Teams):
   ```
   New skill added: $cortex-skills:commonwealth-data-review
   Purpose: Reviews a dataset or workflow before sharing.
   To get it: click Sync on the plugin in Agent Settings, or type "Sync my skills".
   ```
5. **Team members** sync and use the skill.

### Troubleshooting

| Problem | Solution |
| --- | --- |
| Skill does not appear after install | Run `Sync my skills`, then `/skill list` |
| Skill triggers at the wrong time | Tighten the `description` field in SKILL.md |
| Skill never auto-triggers | Add clearer trigger phrases to `description` |
| Only need one skill | Install the single skill path instead of the full repo |
| Testing local changes | Use `/local-plugin-installer` with your local folder path |

---

## Adding a New Skill

1. Copy `skills/_template/` to `skills/<your-skill-name>/`.
2. Rename the folder using lowercase letters and hyphens only.
3. Edit `SKILL.md` — fill in all required frontmatter fields and body sections.
4. Add supporting material under `references/` if needed.
5. Include a `LICENSE` file (copy from the template).
6. Run validation locally:
   ```powershell
   python .github/scripts/validate_skill.py skills/<your-skill-name>
   ```
7. Test the skill in CoCo using `/local-plugin-installer`.
8. Open a pull request. CI will validate automatically.
9. After merge, notify the team to sync.

---

## Current Skills

| Skill | Status | Purpose |
| --- | --- | --- |
| [`commonwealth-data-review`](skills/commonwealth-data-review) | draft | Reviews datasets and workflows before sharing or handoff |
| [`data-ingest-medallion`](skills/data-ingest-medallion) | draft | Automates Snowflake file ingestion using a raw-to-staging medallion pattern |
| [`_template`](skills/_template) | template | Copy this folder when creating a new skill |

---

## Rules

- Do not upload secrets, passwords, tokens, private keys, or connection strings.
- Do not upload protected data or production extracts.
- Keep each skill focused on one reusable workflow.
- Put long examples or checklists in `references/`.
- Use `draft`, `beta`, `stable`, or `archived` for status.
- Test the skill with the example prompt before sharing it.
- Ensure `id` matches the folder name exactly.
- Run `python .github/scripts/validate_skill.py --all` before opening a PR.
