# Team Process For Sharing Skills

This is the lightweight process for using the repo as a shared skill library.

## Roles

| Role | What They Do |
| --- | --- |
| Skill author | Creates or updates a skill folder. |
| Reviewer | Checks clarity, safety, and usefulness. |
| Team member | Installs or syncs the repo in CoCo and uses shared skills. |

## Add A New Skill

1. Start from `skills/_template/`.
2. Create a new folder under `skills/`.
3. Fill out `SKILL.md`.
4. Add supporting material under `references/` if needed.
5. Test the skill locally in CoCo.
6. Upload the folder or open a pull request.
7. Ask one teammate to review it.
8. After it is accepted, tell the team to run `Sync my skills`.

## Update An Existing Skill

1. Edit the skill folder.
2. Keep the same `id` unless this is truly a new skill.
3. Update examples or reference files when behavior changes.
4. Test with the example prompt.
5. Share the update with the team.

## Review A Skill

Reviewers should check:

- Is the purpose clear?
- Is the example prompt useful?
- Does the skill avoid secrets and protected data?
- Is the workflow specific enough to be reusable?
- Are risky actions handled with stopping points?
- Would another team member understand when to use it?

## Team Usage Pattern

When a skill is added or updated:

1. Author posts the skill name and short purpose.
2. Team members run `Sync my skills`.
3. Team members use the skill with `$skill-name`.
4. Feedback becomes a GitHub issue, pull request, or direct edit to the skill folder.

Example message to the team:

```text
New skill added: $commonwealth-data-review
Purpose: Reviews a dataset or workflow before sharing.
To get it: run "Sync my skills" in CoCo.
To use it: $commonwealth-data-review Help me review this workflow.
```

