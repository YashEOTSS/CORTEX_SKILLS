## Skill Submission Checklist

### Scope

- [ ] This PR adds or updates one focused skill.
- [ ] The use case is reusable across projects, teams, or agencies.
- [ ] The PR does not include secrets, credentials, protected data, or production extracts.

### Folder Structure

- [ ] My skill lives at `skills/<skill-id>/`.
- [ ] The folder name matches the `id` field in `SKILL.md`.
- [ ] `SKILL.md` is present.
- [ ] `LICENSE` is present.
- [ ] Longer guidance is placed in `references/` when appropriate.

### Metadata

- [ ] Required frontmatter fields are complete.
- [ ] `status` is one of `draft`, `beta`, `stable`, or `archived`.
- [ ] `owner_agency` identifies the owning team.
- [ ] `data_classification` reflects the intended sharing level.
- [ ] The `description` explains when to use and when not to use the skill.

### Testing

- [ ] I tested the skill with the example prompt.
- [ ] I ran `python .github/scripts/validate_skill.py --all`.
- [ ] The skill behaves as described.

## What This Skill Does

<!-- Briefly describe the skill and who it helps. -->

## Example Prompt

<!-- Include a prompt that should trigger the skill. -->

## Known Limitations

<!-- Describe anything reviewers or users should know. -->

