# Commonwealth Data Review Checklist

Use this checklist when reviewing a dataset, query, notebook, or analysis workflow before sharing.

## Context

- What is the purpose of the dataset or workflow?
- Who owns the data?
- Who is the intended audience?
- Is the sharing internal, cross-agency, vendor-facing, or public?
- What decision or analysis depends on this work?

## Data Quality

- Are required columns present?
- Are column names understandable?
- Are data types clear and consistent?
- Are missing values explained?
- Are duplicate records expected?
- Are date ranges documented?
- Are joins and filters documented?
- Are row counts checked before and after transformations?

## Privacy And Sensitivity

- Does the dataset include direct identifiers?
- Does the dataset include indirect identifiers that could identify a person when combined?
- Does the dataset include protected, confidential, or restricted program information?
- Are aggregation levels appropriate for the intended audience?
- Has the data owner approved the sharing context?

## Reproducibility

- Can another analyst rerun the workflow?
- Are source tables, file names, and date ranges documented?
- Are assumptions written down?
- Are manual steps clearly described?
- Are package or tool dependencies identified?
- Are outputs traceable to inputs?

## Handoff Readiness

- Is there a short summary of what the data contains?
- Are limitations documented?
- Are known caveats visible near the output?
- Is the refresh cadence known?
- Is there a point of contact for questions?
- Are next steps clear?

## Review Result

Use one of these outcomes:

- `ready`: no blockers found.
- `ready with caveats`: usable, but reviewers should see the listed concerns.
- `not ready`: blockers should be resolved before sharing.

