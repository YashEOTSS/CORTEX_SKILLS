# Proposal: ODIA Shared Cortex Skills Repository

## Purpose

ODIA can use a shared GitHub repository to collect, review, and distribute Cortex Skills developed by analysts, engineers, and partner teams across the Commonwealth. The repository gives teams a standard place to package reusable workflows instead of leaving them in individual chats, local folders, notebooks, or one-off documentation.

The model follows the Snowflake Labs Cortex Code skills repository: each skill is a folder with a `SKILL.md` file, license, examples, and optional supporting material.

## Why This Is Useful

Commonwealth teams often solve similar problems:

- Reviewing datasets before analysis
- Documenting Snowflake access patterns
- Checking grant, finance, or program data quality
- Creating repeatable analytics workflows
- Explaining agency-specific domain logic
- Translating standards into step-by-step assistant behavior

A shared Cortex Skills repo turns those workflows into reusable assets. Analysts can install or reference a skill, use it in a Cortex session, improve it, and submit changes through a pull request.

## Proposed Repository Model

```text
CORTEX_SKILLS/
  README.md
  CONTRIBUTING.md
  docs/
    proposal.md
    governance.md
    sample-walkthrough.md
  skills/
    _template/
      SKILL.md
      LICENSE
      references/
      scripts/
      assets/
    <skill-id>/
      SKILL.md
      LICENSE
      references/
      scripts/
      assets/
  .github/
    PULL_REQUEST_TEMPLATE.md
    workflows/
      validate-skill.yml
    scripts/
      validate_skill.py
```

## Skill Folder Standard

Each skill is self-contained:

```text
skills/commonwealth-data-review/
  SKILL.md
  LICENSE
  references/
    review-checklist.md
```

`SKILL.md` should explain when the skill applies, what workflow it follows, what tools it can use, and where it should stop for human review.

Long policy text, checklists, examples, or standards should live in `references/` so the main skill stays focused.

## Recommended Metadata

Each skill should include these fields:

- `id`
- `name`
- `title`
- `summary`
- `description`
- `authors`
- `owner_agency`
- `status`
- `categories`
- `data_classification`
- `tools`
- `prompt`
- `language`

This gives ODIA enough information to catalog skills, review ownership, understand maturity, and avoid unsafe sharing.

## Governance Model

| Role | Responsibility |
| --- | --- |
| Contributor | Creates or updates a skill and tests it locally. |
| Reviewer | Checks clarity, safety, metadata, and usefulness. |
| Maintainer | Approves standards, merges pull requests, and manages repo structure. |
| Skill owner | Keeps a specific skill accurate over time. |

## Skill Lifecycle

```text
draft -> beta -> stable -> archived
```

- `draft`: early version for discussion
- `beta`: tested and usable, but still being refined
- `stable`: reviewed and recommended for reuse
- `archived`: retained for history but no longer recommended

## Initial Implementation

The first version of the repository should include:

- Root README explaining the purpose and structure
- Contribution guide
- Skill template
- One sample ODIA-style skill
- Proposal and walkthrough docs
- Pull request template
- GitHub Action that validates skill folders

This is enough to satisfy the initial ticket with a local repo walkthrough while setting up a path for the real organization repository.

## Future Enhancements

- Publish a formal skill catalog page
- Add tags for domains such as grants, finance, public health, transportation, workforce, and education
- Add automated checks for secrets and large files
- Add reviewers by category or agency
- Add examples showing how to install from the final GitHub organization URL
- Add a release process for stable skill versions

