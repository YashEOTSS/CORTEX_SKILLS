# ODIA Cortex Skills

This repository is a shared catalog for Cortex Skills developed by ODIA and partner teams across the Commonwealth. It follows the same basic shape as the Snowflake Labs Cortex Code skills repository: each reusable skill lives in its own folder under `skills/`, with a `SKILL.md`, license, examples, and optional reference files.

The goal is to make useful analyst and engineering workflows easy to discover, review, improve, and reuse.

## What Belongs Here

- Reusable Cortex Skills for Commonwealth analytics, data engineering, governance, and Snowflake workflows
- Skill templates that help teams package repeatable work
- Reference checklists, examples, and helper scripts that are safe to share
- Draft skills that need peer review before broader use

Do not commit credentials, secrets, production extracts, protected data, or agency-specific material that is not approved for sharing.

## Skill Catalog

| Skill | Status | What it does |
| --- | --- | --- |
| [`commonwealth-data-review`](skills/commonwealth-data-review) | draft | Sample skill showing how ODIA analysts can package a reusable data review workflow. |
| [`_template`](skills/_template) | template | Starter folder for new skills. Copy this folder when creating a new skill. |

## Repo Structure

```text
.
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── proposal.md
│   ├── governance.md
│   └── sample-walkthrough.md
├── skills/
│   ├── _template/
│   │   ├── SKILL.md
│   │   ├── LICENSE
│   │   ├── references/
│   │   ├── scripts/
│   │   └── assets/
│   └── commonwealth-data-review/
│       ├── SKILL.md
│       ├── LICENSE
│       └── references/
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── scripts/
    │   └── validate_skill.py
    └── workflows/
        └── validate-skill.yml
```

## Authoring A Skill

1. Copy `skills/_template/` into `skills/<your-skill-id>/`.
2. Rename the folder using lowercase letters, numbers, and hyphens.
3. Fill out the frontmatter in `SKILL.md`.
4. Add examples, references, helper scripts, or assets only when they make the skill easier to use.
5. Test the skill locally against the example prompt.
6. Open a pull request using the checklist in `.github/PULL_REQUEST_TEMPLATE.md`.

Every skill should be focused, reusable, and safe to share across teams.

## Required Skill Metadata

Each `SKILL.md` must include these fields:

```yaml
---
id: commonwealth-data-review
name: commonwealth-data-review
title: Commonwealth Data Review
summary: Helps analysts review datasets before sharing or analysis.
description: Use when reviewing a dataset, validation notebook, or repeatable analysis workflow.
authors: ODIA Team
owner_agency: EOTSS / ODIA
status: draft
categories:
  - analytics
  - data-quality
data_classification: internal
tools:
  - Read
  - Grep
  - Bash
prompt: Help me review this dataset workflow.
language: en
---
```

Valid statuses are `draft`, `beta`, `stable`, and `archived`.

## Local Validation

Run this before opening a pull request:

```powershell
python .github/scripts/validate_skill.py --all
```

The validator checks required files, required metadata, folder naming, status values, license markers, and common safety issues.

## Ticket Artifacts

The planning artifacts for the initial ODIA repository proposal are in:

- [docs/proposal.md](docs/proposal.md)
- [docs/sample-walkthrough.md](docs/sample-walkthrough.md)
- [docs/governance.md](docs/governance.md)

