---
id: commonwealth-data-review
name: commonwealth-data-review
title: Commonwealth Data Review
summary: Helps analysts review datasets and analysis workflows before sharing or reuse.
description: |
  Use when an analyst needs to review a dataset, notebook, SQL workflow, or analysis package before sharing it with another team. The skill checks data quality, metadata, privacy concerns, reproducibility, ownership, and handoff readiness. Triggers include dataset review, data quality review, analysis handoff, share this dataset, review my workflow, Commonwealth data review, and ODIA review checklist. Do not use for legal approval, production access changes, or final data classification decisions.
authors: ODIA Team
owner_agency: EOTSS / ODIA
status: draft
categories:
  - analytics
  - data-quality
  - governance
data_classification: internal
tools:
  - Read
  - Grep
  - Bash
prompt: Help me review this dataset workflow before I share it with another team.
language: en
---

# Commonwealth Data Review

## Overview

This sample skill shows how ODIA could package a reusable analyst workflow. It helps review a dataset or analysis workflow before it is shared, reused, or handed off to another team.

The goal is not to approve the data for release. The goal is to create a consistent pre-review that surfaces quality, privacy, reproducibility, and documentation gaps.

## When To Use

Use this skill when a user asks to:

- Review a dataset before sharing it.
- Check whether an analysis workflow is reproducible.
- Identify missing metadata or unclear assumptions.
- Prepare a handoff note for another analyst or agency partner.
- Find data quality risks before publishing outputs.

## When Not To Use

Do not use this skill for:

- Final legal approval.
- Final public records or privacy determinations.
- Granting Snowflake access.
- Running production data changes.
- Certifying official statistics.

## Workflow

1. Confirm the intended audience, sharing context, and owner agency.
2. Inspect available files, schemas, queries, notebooks, or documentation.
3. Use `references/review-checklist.md` to evaluate the workflow.
4. Summarize findings by severity: blockers, concerns, and improvements.
5. Recommend next steps for the analyst or data owner.

## Output Format

Return a concise review with these sections:

- `Decision`: ready, ready with caveats, or not ready.
- `Blockers`: issues that should be fixed before sharing.
- `Concerns`: risks that need owner or reviewer attention.
- `Improvements`: helpful but non-blocking cleanup.
- `Questions`: information needed from the analyst or data owner.
- `Suggested Handoff Note`: short text the analyst can reuse.

## References

- `references/review-checklist.md`

## Stopping Points

Stop and ask for human confirmation before:

- Recommending external sharing.
- Treating a dataset as public or unrestricted.
- Modifying files, queries, tables, or access controls.
- Making a final classification call.

## Common Mistakes

- Assuming missing values are harmless without domain context.
- Treating synthetic examples and production extracts the same way.
- Sharing derived outputs without confirming data owner expectations.
- Forgetting to document filters, joins, and time periods.
- Recommending reuse when the source system or refresh cadence is unclear.

