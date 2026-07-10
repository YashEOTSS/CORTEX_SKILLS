# Governance Guide

This guide describes how ODIA can manage shared Cortex Skills safely and consistently.

## Principles

- Skills should be reusable, not one-off notes.
- Skills should be safe to inspect and run.
- Skills should avoid sensitive data, secrets, and credentials.
- Skills should have clear owners.
- Skills should improve through pull request review.
- Skills should be retired when they are no longer accurate.

## Data Safety

Do not commit:

- Passwords, tokens, keys, certificates, or connection strings
- Production data extracts
- Protected personal information
- Agency-restricted documents unless explicitly approved
- Screenshots containing sensitive information
- Generated outputs that expose confidential data

Use realistic synthetic examples instead of real records.

## Ownership

Every skill should identify:

- Author or team
- Owning agency or ODIA unit
- Expected audience
- Current status
- Known limitations

Ownership matters because skills can become stale when policies, schemas, tools, or Snowflake objects change.

## Review Gates

Before a skill moves to `stable`, reviewers should confirm:

- The skill solves a clear Commonwealth use case.
- The workflow can be followed by someone who did not write it.
- The skill has been tested with at least one realistic prompt.
- The skill does not duplicate an existing skill without a reason.
- The skill includes appropriate stopping points before risky actions.
- The skill does not include sensitive data or operational secrets.

## Status Changes

Status changes should happen through pull requests.

| Change | Minimum Evidence |
| --- | --- |
| `draft` to `beta` | Another person tested the skill and confirmed it works for the stated use case. |
| `beta` to `stable` | Reviewers confirm clarity, safety, and repeatability. |
| Any status to `archived` | The skill is replaced, obsolete, unsafe, or no longer maintained. |

## Review Cadence

ODIA maintainers should periodically review stable skills for:

- Accuracy
- Ownership
- Broken links
- Deprecated Snowflake or Cortex behavior
- Outdated agency terminology
- Missing examples

Quarterly review is a reasonable starting point for high-use skills.

