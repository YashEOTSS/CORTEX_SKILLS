# Using Team Skills In CoCo

This document explains how team members can install, sync, and use skills from this repository in Cortex Code / CoCo.

## Install The Whole Repo

In CoCo, ask:

```text
Install the skills from https://github.com/<org>/<repo>
```

Replace `<org>/<repo>` with the final GitHub repository path.

For local testing, use the local folder path:

```text
Install the skills from C:\Users\Yash.Malviya\OneDrive - Commonwealth of Massachusetts\Desktop\COMO COCO\CORTEX_SKILLS
```

## Install One Skill

Use this when you only want one skill:

```text
Install the skill at https://github.com/<org>/<repo>/tree/main/skills/<skill-name>
```

Local example:

```text
Install the skill at C:\Users\Yash.Malviya\OneDrive - Commonwealth of Massachusetts\Desktop\COMO COCO\CORTEX_SKILLS\skills\commonwealth-data-review
```

## Sync Updates

When someone adds or updates a skill in GitHub, run:

```text
Sync my skills
```

This tells CoCo to pull the latest version of the installed skills.

## See Available Skills

Run:

```text
/skill list
```

You can also open the skill picker:

```text
/skill
```

## Use A Shared Skill

Invoke a skill by name:

```text
$<skill-name> <your task>
```

Example:

```text
$commonwealth-data-review Help me review this dataset workflow before I share it with another team.
```

## Recommended Team Workflow

1. Install the repo once.
2. Run `/skill list` to confirm the skills are available.
3. Use `$skill-name` when you want a specific shared workflow.
4. Run `Sync my skills` when someone announces a new or updated skill.
5. Improve skills through GitHub rather than editing local cached copies.

## Troubleshooting

| Problem | What To Try |
| --- | --- |
| A new skill does not appear | Run `Sync my skills`, then `/skill list`. |
| A skill triggers at the wrong time | Tighten the `description` in `SKILL.md`. |
| A skill never triggers automatically | Add clearer trigger phrases to `description`. |
| You only need one skill | Install the single skill path instead of the full repo. |
| You are testing locally | Install from the local `skills/<skill-name>` path. |

