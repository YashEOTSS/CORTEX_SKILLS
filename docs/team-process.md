# Team Process

For full documentation, see the [README](../README.md).

## Roles

| Role | Responsibility |
| --- | --- |
| Skill author | Creates or updates a skill folder and opens a PR |
| Reviewer | Checks clarity, safety, and usefulness. Ensures CI passes |
| Team member | Syncs the plugin and uses shared skills |

## Review Checklist

When reviewing a skill PR, check:

- Is the purpose clear from the title and description?
- Does the example prompt produce useful output?
- Are secrets, protected data, or production extracts absent?
- Is the workflow specific enough to be reusable?
- Are risky actions gated behind stopping points?
- Does CI validation pass?
