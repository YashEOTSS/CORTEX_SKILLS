# Contributing To ODIA Cortex Skills

This repo is designed to make Cortex Skills reusable across ODIA and Commonwealth teams. A contribution should package a repeatable workflow so another analyst or engineer can understand it, test it, and improve it through normal GitHub review.

## Before You Start

Ask these questions before creating a skill:

- Is this workflow reusable by more than one person or project?
- Can it be explained without sensitive data or credentials?
- Does it have a clear example prompt?
- Does it fit one focused use case?
- Can another reviewer test the behavior?

If the answer is no, keep iterating locally before submitting.

## Create A New Skill

1. Copy `skills/_template/` into `skills/<skill-id>/`.
2. Use a lowercase, hyphenated folder name such as `grant-quality-review`.
3. Update `SKILL.md` so the `id` and `name` match the folder name.
4. Keep the main `SKILL.md` concise. Move longer material into `references/`.
5. Add helper scripts only if they are necessary and safe to run.
6. Add examples that show realistic inputs and expected outputs.
7. Run local validation.

```powershell
python .github/scripts/validate_skill.py --all
```

## Required Files

Each real skill folder must include:

```text
skills/<skill-id>/
  SKILL.md
  LICENSE
```

Optional supporting folders:

```text
references/   Longer instructions, checklists, examples, standards
scripts/      Helper scripts used by the skill
assets/       Small templates, fixtures, or safe sample files
```

## Required Frontmatter

Each `SKILL.md` must include:

| Field | Purpose |
| --- | --- |
| `id` | Stable skill identifier. Must match the folder name. |
| `name` | Invocation name. Usually the same as `id`. |
| `title` | Human-readable display name. |
| `summary` | One short sentence explaining the skill. |
| `description` | When to use the skill, trigger terms, and nearby cases it should not handle. |
| `authors` | Person or team responsible for the contribution. |
| `owner_agency` | Owning team or agency. |
| `status` | `draft`, `beta`, `stable`, or `archived`. |
| `categories` | At least one classification tag. |
| `data_classification` | Expected sharing level, such as `public`, `internal`, or `restricted`. |
| `tools` | Tools the skill expects to use. |
| `prompt` | Example prompt that should activate the skill. |
| `language` | Language code, usually `en`. |

## Status Lifecycle

| Status | Meaning |
| --- | --- |
| `draft` | Early version. Good enough to discuss, not broadly recommended. |
| `beta` | Tested by at least one other person. Useful, but still being refined. |
| `stable` | Reviewed, tested, and ready for general reuse. |
| `archived` | Kept for history, replaced by another skill, or no longer recommended. |

## Review Checklist

Reviewers should confirm:

- The use case is clear and reusable.
- The skill does not contain secrets, credentials, or sensitive data.
- The `description` is specific enough to avoid accidental activation.
- The example prompt works as described.
- Any scripts are understandable, scoped, and safe to run.
- Longer guidance is placed in `references/`.
- The status reflects the maturity of the skill.

## Pull Requests

Use small pull requests when possible. One new skill or one meaningful update is easier to review than a large mixed change.

Every pull request should explain:

- What the skill does
- Who it helps
- How it was tested
- Any known limitations
- Whether it is ready for `draft`, `beta`, or `stable`

