# Contributing

Thank you for your help. Improvements are welcome.

## Good changes

- Example ladders for more topics and ages (`references/examples.md`).
- Curriculum notes for other countries or UK nations. Add a new file in `references/` and tell `SKILL.md` when to read it.
- Corrections to the curriculum summary or the pure sounds guide.
- Fixes to the skill rules, when a real session shows a problem.

## Rules for the skill

- Keep the privacy rules. The skill must not save full names, school names, addresses, dates of birth or photos.
- Keep the learner data in `learner/`. Do not commit learner data. Do not add real data about a child to examples.
- Write in UK English. Use short, simple sentences. The skill text uses ASD-STE100 Simplified Technical English where possible.
- Keep `SKILL.md` short. Put long reference content in `references/`.
- Keep the skill description at 200 characters or fewer. Claude does not accept a longer description for upload.

## Steps

1. Fork the repository and make a branch.
2. Edit the files in `plugins/young-tutor/skills/young-tutor/`.
3. Make the ZIP file again: `python3 scripts/package_skill.py`
4. Do the checks: `python3 scripts/validate.py`
5. If you change the skill, increase `version` in `plugins/young-tutor/.claude-plugin/plugin.json`.
6. Open a pull request. Tell us what you changed and why. If you tested the change in a real session, tell us the age of the child and what happened. Do not give names.

The GitHub workflow does the same checks on each pull request.
