# Contributing Skills

Use this guide when adding or updating a skill in this repo.

## Folder Pattern

Each skill gets one folder:

```text
skills/<skill-name>/
  SKILL.md
  LICENSE
  references/
```

Optional folders:

```text
scripts/    Helper scripts used by the skill
assets/     Small templates or safe sample files
```

## Create A Skill

1. Copy `skills/_template/`.
2. Rename it to your skill name, for example `skills/monthly-report-review/`.
3. Update the frontmatter in `SKILL.md`.
4. Write the workflow instructions.
5. Add longer notes or checklists to `references/`.
6. Test it in CoCo.
7. Submit the folder through GitHub.

## Required `SKILL.md` Fields

```yaml
---
id: monthly-report-review
name: monthly-report-review
title: Monthly Report Review
summary: Helps review monthly report outputs before sharing.
description: |
  Use when a user needs help reviewing monthly report outputs,
  assumptions, source checks, and handoff notes.
authors: Your Name or Team Name
status: draft
tools:
  - Read
  - Grep
prompt: Help me review this monthly report before I send it.
language: en
---
```

Optional fields:

```yaml
categories:
  - analytics
  - reporting
```

## Status Values

| Status | Meaning |
| --- | --- |
| `draft` | New skill. Ready for team review or testing. |
| `beta` | Tested by at least one other person. |
| `stable` | Ready for routine team use. |
| `archived` | Kept for history but no longer recommended. |

## Testing In CoCo

Install a local skill while developing:

```text
Install the skill at C:\path\to\repo\skills\<skill-name>
```

Use it:

```text
$<skill-name> <your prompt>
```

After a skill is merged or uploaded to GitHub, teammates should run:

```text
Sync my skills
```

## Review Checklist

Before sharing a skill, confirm:

- The skill solves one clear workflow.
- The example prompt works.
- The skill does not contain secrets or sensitive data.
- The folder name matches the `id`.
- Long reference material is in `references/`.
- Any scripts are safe and explained.

