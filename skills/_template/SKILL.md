---
id: replace-with-skill-id
name: replace-with-skill-id
title: Replace With Skill Title
summary: One sentence describing what this skill helps users do.
description: |
  Use when a user needs help with the specific workflow this skill supports.
  Include trigger terms and adjacent cases this skill should not handle.
authors: ODIA Team
status: draft
categories:
  - replace-category
tools:
  - Read
  - Grep
prompt: Replace with an example prompt that should activate the skill.
language: en
---

# Replace With Skill Title

## Overview

Describe the reusable workflow this skill packages and who it is for.

## When To Use

Use this skill when:

- The user asks for the workflow this skill supports.
- The task is repeatable across projects or teams.
- The workflow can be completed without exposing sensitive data.

## When Not To Use

Do not use this skill when:

- The request depends on credentials, secrets, or restricted data.
- The user needs a one-off answer rather than a reusable workflow.
- A more specific skill already covers the task.

## Workflow

1. Confirm the user goal and available inputs.
2. Inspect the relevant files, schema, or documentation.
3. Follow the supporting checklist or reference material.
4. Produce a concise recommendation, output, or next-step plan.
5. Stop for human approval before taking risky actions.

## References

- `references/README.md`

## Common Mistakes

- Making the skill too broad.
- Including sensitive examples.
- Omitting a test prompt.
- Skipping stopping points for risky actions.

## Stopping Points

Stop and ask for confirmation before:

- Sharing data externally
- Running write operations
- Changing production objects
- Making access, permission, or policy recommendations that need owner approval
