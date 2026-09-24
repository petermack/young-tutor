# young-tutor

A Claude skill that tutors a young child on a topic that a parent gives. The skill changes the method and the difficulty to suit the age and the results of the child.

## What the skill does

- **First use:** Claude asks the parent for a nickname, the age, the country and the interests of the child. Claude saves them in `learner/profile.json`. Claude does not save full names or school names.
- **New topic:** Claude makes a ladder of 5 to 8 levels that suit the age of the child. For UK school topics, Claude aligns the ladder to EYFS or KS1. Claude asks which programme the school uses (for example, the phonics scheme).
- **Children under 7:** Claude talks to the parent. The parent reads aloud and types the answers of the child. Sessions are 5 to 10 minutes, with one new idea. Claude uses games, pictures and household objects, and praises effort. For phonics, Claude tells the parent which pure sounds to say.
- **During a lesson:**
  - 2 correct answers in a row: Claude goes up one level.
  - 2 incorrect answers in a row: Claude goes down one level.
  - Signs of confusion (guesses, "I don't know", the same error again): Claude changes the method. Claude uses a real example, smaller steps or a simpler question.
- **Progress:** Claude saves each topic in `learner/progress/<topic>.json`: the level, what worked, what did not work and the next step. Claude reads the profile and the progress at the start of each session.
- **Style:** UK English. Warm and simple. Hints before answers.

## What you need

- The Claude Desktop app with Cowork, and a paid Claude plan (Pro, Max, Team or Enterprise).
- The setting "Code execution and file creation" on. Go to **Settings > Capabilities**.
- A folder on your computer for the learner files.

## Install in Claude Cowork

Use Option A or Option B. Do not use both.

### Option A: add this repository as a plugin marketplace

1. Open the Claude Desktop app. Select the **Cowork** tab.
2. Select **Customize**, then **Plugins**.
3. In **Personal plugins**, select **+**. Select **Add marketplace**, then **Add from a repository**.
4. Type `petermack/young-tutor`.
5. Find **young-tutor** in the list of plugins. Select **Install**.

Cowork must be able to read this repository. If the repository is private and Cowork cannot read it, make the repository public or use Option B.

To update: go to **Customize > Plugins**, find the **young-tutor** marketplace and select **Update**.

### Option B: upload the skill as a ZIP file

1. Get the ZIP file. On GitHub, open [`dist/young-tutor.zip`](dist/young-tutor.zip) and select the download button. Do not unzip the file.
2. In Claude, go to **Settings > Capabilities**. Make sure that **Code execution and file creation** is on.
3. Go to **Customize > Skills**. Select **+**, then **Create skill**, then **Upload a skill**.
4. Select `young-tutor.zip`.
5. Make sure that the **young-tutor** skill is on.

Skills that you turn on in Claude also work in Cowork.

To update: remove the old skill, then upload the new ZIP file.

### Claude Code (optional)

```
/plugin marketplace add petermack/young-tutor
/plugin install young-tutor@young-tutor
```

## First session

1. Make a folder on your computer. For example: `Documents/Young Tutor`.
2. In Cowork, start a new task and select this folder. Select the same folder each time. The skill keeps the progress of the child in this folder.
3. Type a request. For example: "Start a young tutor session" or "I want to help my child with phonics."
4. Claude asks four questions: the nickname, the age, the country and the interests of the child.
5. Give a topic. Claude makes a ladder of levels and shows it to you. Tell Claude where your child is now.
6. For a child under 7:
   - Do the **Parent:** steps.
   - Read the **Say:** lines aloud to your child.
   - **Type** what your child says or does. Also type "I don't know" and wrong answers. If you helped, type "(helped)".

## Files that the skill makes

```
Young Tutor/                  <- the folder that you select in Cowork
└── learner/
    ├── profile.json          nickname, age, country, school year (optional), interests
    └── progress/
        ├── phonics.json      ladder, level, what worked, what did not work, next step
        └── number-bonds-to-10.json
```

To start again, delete the `learner` folder.

## Privacy

- The skill does not save full names, school names, addresses, dates of birth or photos.
- The learner files stay in the folder that you select. Your conversations with Claude follow the normal Claude privacy terms.
- `learner/` is in `.gitignore`. If your working folder is a Git repository, the skill adds `learner/` to its `.gitignore`.

## Repository layout

```
.claude-plugin/marketplace.json            Marketplace for Cowork and Claude Code
plugins/young-tutor/
├── .claude-plugin/plugin.json             Plugin manifest
└── skills/young-tutor/
    ├── SKILL.md                           The skill
    └── references/
        ├── uk-eyfs-ks1.md                 EYFS and KS1 summary, phonics and maths programmes
        ├── phonics-pure-sounds.md         Pure sounds guide for the parent
        └── examples.md                    Example ladders and an example session
dist/young-tutor.zip                       Skill ZIP file for upload (Option B)
scripts/package_skill.py                   Makes the ZIP file
scripts/validate.py                        Checks the skill, the manifests and the ZIP file
```

## Change the skill

1. Edit the files in `plugins/young-tutor/skills/young-tutor/`.
2. Make the ZIP file again: `python3 scripts/package_skill.py`
3. Do the checks: `python3 scripts/validate.py`
4. Increase `version` in `plugins/young-tutor/.claude-plugin/plugin.json`. Cowork uses the version to find updates.
5. Commit and push.

The GitHub workflow does the checks on each push.

## Limits

- The skill does not replace school. If you are worried about the learning of your child, speak to the class teacher or the school SENCO.
- The curriculum notes are a short summary. For the full text, see the EYFS statutory framework and the national curriculum in England on [GOV.UK](https://www.gov.uk/).
