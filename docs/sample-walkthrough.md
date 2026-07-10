# Sample Walkthrough: Contributing A Cortex Skill

This walkthrough shows how the ODIA repo could work using the local sample skill.

## Scenario

An analyst has a repeatable process for reviewing a dataset before sharing it with another team. The workflow includes checking columns, missing values, sensitive fields, assumptions, and reproducibility notes.

Instead of keeping the workflow in a personal note, the analyst packages it as a Cortex Skill.

## Step 1: Start From The Template

Copy the template folder:

```powershell
Copy-Item -Recurse skills/_template skills/commonwealth-data-review
```

Rename fields in `skills/commonwealth-data-review/SKILL.md` so the `id` and `name` match the folder name.

## Step 2: Write The Skill

The analyst fills in:

- What the skill does
- When to use it
- When not to use it
- The workflow steps
- Required human stopping points
- A link to `references/review-checklist.md`

## Step 3: Add Supporting Material

The detailed review checklist lives at:

```text
skills/commonwealth-data-review/references/review-checklist.md
```

This keeps the main `SKILL.md` readable while preserving enough detail for reviewers.

## Step 4: Validate Locally

Run:

```powershell
python .github/scripts/validate_skill.py --all
```

The validator checks that each real skill has:

- `SKILL.md`
- `LICENSE`
- Required metadata
- Matching folder name and `id`
- Valid status
- No obvious secret placeholders

## Step 5: Open A Pull Request

The analyst opens a PR and completes the checklist:

- Why the skill is useful
- Who should use it
- How it was tested
- Whether it includes sensitive data
- What status it should have

## Step 6: Review And Merge

Reviewers check the skill for:

- Clarity
- Safety
- Reusability
- Metadata quality
- Fit with existing skills

If accepted, the skill becomes part of the shared ODIA catalog.

## Demo Prompt

The sample skill can be tested with a prompt like:

```text
$commonwealth-data-review Help me review this dataset workflow before I share it with another team.
```

Expected behavior:

1. The assistant asks for or inspects the relevant dataset/workflow context.
2. It follows the review checklist.
3. It flags missing metadata, data quality risks, privacy concerns, and reproducibility gaps.
4. It stops before recommending external sharing if classification or ownership is unclear.

