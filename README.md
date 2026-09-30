# Merge Conflict Studio

## Overview
Merge conflicts are a normal part of working on a team. In this studio you will cause, and then resolve, several merge conflicts in a small command-line task manager (the same design you saw in the Workflow Practice studio). The first rounds walk you through every command. Each later round gives you less help, so by the end you are resolving conflicts on your own.

| Round | What you practice | Where you resolve | Scaffolding |
|---|---|---|---|
| 1 | Reading conflict markers; choosing a resolution | GitHub web editor | Every step spelled out |
| 2 | Resolving several conflicts across files, locally | Your editor + terminal | Commands given, explanation reduced |
| 3 | Writing your own code that collides with a teammate's | Your choice | Feature ticket + checklist only |
| 4 | A conflict Git **can't** see | — | One paragraph |

## Roles and merge order
Work in a group of **2 or 3**. Pick roles now and write them here:

* Person A: ______
* Person B: ______
* Person C *(3-person groups only)*: ______

In every round, everyone makes a change on their **own branch** and opens a pull request (PR) to `main`. PRs are merged **one at a time, in the order below**. The first PR in a round merges cleanly. Every PR after that one has a conflict, and its author resolves it. The order rotates so everyone gets to resolve conflicts.

| Round | 3-person merge order | 2-person merge order |
|---|---|---|
| 1 | A → **B** → **C** | A → **B** |
| 2 | B → **C** → **A** | B → **A** |
| 3 | C → **A** → **B** | A → **B** |
| 4 | A → B (C: tester) | A → B |

**Bold** = you will resolve a conflict in that round.

**Rules for every round**
1. At the start of a round, **everyone** updates `main` first: `git checkout main` then `git pull`.
2. Do **not** merge your PR until the person before you has merged theirs.
3. After every merge, someone runs the tests and the program on the updated `main`:
   ```
   python -m unittest
   python main.py
   ```
   (Use `python3` if `python` doesn't work on your machine.)

---

## Setup (everyone, ~5 min)
1. Clone your team repository and `cd` into it.
2. Run `python -m unittest`. You should see `OK`.
3. Run `python main.py`. Add a task, list it, then quit. Look around `ui/cli.py` and `entity/task.py`; these are the two files you will fight over.
4. One person: fill in the roles above and commit the change **directly to `main`**, then push. Everyone else runs `git pull`. (Tiny setup edits like this are the only time we skip a PR.)

---

## Round 1: Your first conflict (fully guided, resolve on GitHub)

**The story:** Everyone thinks the message printed after adding a task could be better, and each of you "fixes" it differently. You all edit the **same line** of `ui/cli.py`.

### 1.1 Make your change (everyone)
Replace `X` with your role letter (`a`, `b`, or `c`) in the branch name and the patch name:
```
git checkout main
git pull
git checkout -b round1-X
git apply rounds/round1/X.patch
git diff
```
`git diff` shows the one line your patch changed. Read it so you know what *your* version does.

Commit and push:
```
git add ui/cli.py
git commit -m "Improve add-task confirmation message"
git push --set-upstream origin round1-X
```

### 1.2 Open your PR (everyone)
On GitHub: **Pull requests → New pull request**, **base: `main`**, **compare: `round1-X`**. Give it a one-sentence description and click **Create pull request**. Don't merge yet!

### 1.3 Merge in order
**Person A** (first in the merge order): your PR says *"This branch has no conflicts with the base branch."* Click **Merge pull request**, then **Confirm merge**.

**Person B** (next): open **your** PR (`round1-b` → `main`) and refresh the page. It now says *"This branch has conflicts that must be resolved."* That happened because `main` changed (A's PR) on the same line your branch changed. Git can't know which version you want, so it asks a human.

Click **Resolve conflicts** on that PR. GitHub opens an editor showing something like this:

```python
        response = self.add_task(AddTaskRequest(description))
<<<<<<< round1-b
        print(f"Added task: {response.task.description}")
=======
        print(f"Task added successfully! (ID: {response.task.id})")
>>>>>>> main
```

| Marker | Meaning |
|---|---|
| `<<<<<<< round1-b` | Start of the conflict. The lines below are **your branch's** version (sometimes called *current* or *ours*). |
| `=======` | Divider. |
| `>>>>>>> main` | End of the conflict. The lines just above are the version **already on `main`** (*incoming* or *theirs*). |

### 1.4 Decide together
Before you edit anything, **talk it over as a group** (30 seconds):
* What was each version trying to achieve?
* Should we keep **ours**, keep **theirs**, or **combine** them?

Here, both changes are good ideas. One adds the ID, the other adds the description. A combined line keeps both, for example:
```python
        print(f"Task #{response.task.id} added: {response.task.description}")
```

### 1.5 Resolve (Person B, in the browser, on **your own PR**)
Everything in this step happens on GitHub, in the editor that opened when you clicked **Resolve conflicts** on **your** PR (`round1-b` → `main`). You don't need your terminal or local clone.

Where does the fix go? It is saved to **your branch, `round1-b`**. GitHub creates a *merge commit* on `round1-b` that brings in the latest `main` and includes your resolution. Nothing changes on `main` until you merge the PR in the last step.

1. In the editor, replace everything from the `<<<<<<< round1-b` line through the `>>>>>>> main` line with the line (or lines) your group agreed on.
2. Make sure **no** `<<<<<<<`, `=======`, or `>>>>>>>` lines remain, and the indentation matches the line above.
3. Click **Mark as resolved** (top right of the editor), then **Commit merge**. If GitHub asks where to commit, choose to commit directly to `round1-b`.
4. You're back on your PR, which now says *no conflicts*. Click **Merge pull request** → **Confirm merge**. **Now** your resolution reaches `main`.

> Your local `round1-b` branch is now behind the one on GitHub. That's fine, because you won't use it again. Each round starts from a fresh `main`.

**Person C** (3-person groups): now repeat 1.3 to 1.5 on **your** PR (`round1-c` → `main`). Your resolution is committed to `round1-c`. This time the `main` side of the conflict is the line your group just agreed on. Decide whether your version adds anything worth keeping.

### 1.6 Verify (whoever merged last)
```
git checkout main
git pull
python -m unittest
python main.py
```
Add a task and check the message. **Did the program still run?** If not, fix it on a new branch and PR it.

---

## Round 2: Several conflicts, resolved locally (guided)

**The story:** Three teammates each add a new field to `Task` and show it in the task list:
* **A** adds `completed_date` (filled in when a task is completed)
* **B** adds `priority` (defaults to `"normal"`)
* **C** adds `due_date` (defaults to none)

All of you change the `Task` constructor **and** the list-printing line in `ui/cli.py`. Each patch also adds a small test file. You will resolve these conflicts **on your own machine**. That is what you'll do most of the time on your project, since the GitHub editor can't handle complicated conflicts.

### 2.1 Make your change and open a PR (everyone)
```
git checkout main
git pull
git checkout -b round2-X
git apply rounds/round2/X.patch
python -m unittest
git add -A
git commit -m "Add <your field> to Task"
git push --set-upstream origin round2-X
```
Open a PR from `round2-X` into `main`. **Merge order this round: B → C → A** (2-person groups: B → A).

### 2.2 First person merges
Person B: your PR has no conflicts. Merge it.

### 2.3 Resolve locally (next person)
Your PR now shows a conflict. **Do not** use the GitHub button this time. Instead, bring the new `main` into your branch on your machine:
```
git checkout main
git pull
git checkout round2-X
git merge main
```
**Two files now have conflicts: `entity/task.py` and `ui/cli.py`.** Git tells you this in two places:

1. **Right after `git merge main`**, in the terminal output:
   ```
   CONFLICT (content): Merge conflict in entity/task.py
   CONFLICT (content): Merge conflict in ui/cli.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```
2. **Any time you run `git status`**, under **"Unmerged paths"**:
   ```
   Unmerged paths:
   	both modified:   entity/task.py
   	both modified:   ui/cli.py
   ```

(`git status` may also list your teammate's new test file under "Changes to be committed". Git merged that file on its own, so you can leave it alone.)

Open both files in your editor and find every `<<<<<<<`. VS Code highlights each conflict and offers *Accept Current / Accept Incoming / Accept Both* above it.

Locally, the top half of each conflict is labeled `HEAD`, which means **your branch**. The bottom half is labeled `main`. For example, C's `entity/task.py` looks like this:
```python
    def __init__(self, description: str, id: int, completed: bool = None, created_date: date = None,
<<<<<<< HEAD
                 due_date: date = None):
=======
                 priority: str = "normal"):
>>>>>>> main
```

**Watch out:** "keep both" is the right *idea* here, but *Accept Both* just stacks the two lines. That gives a parameter list ending in `):` twice, which is a syntax error. After accepting both, **edit the result by hand** so there is one parameter list containing every field:
```python
                 due_date: date = None, priority: str = "normal"):
```
Do the same for the `self.<field> = <field>` lines. In `ui/cli.py`, make the printed line show **all** the new fields.

**Checklist before you commit**
- No conflict markers left: `git diff --check` prints nothing, and searching for `<<<<<<<` finds nothing
- `python -m unittest` passes (your test file **and** your teammates' tests run)
- `python main.py` works: add a task, complete it, list it, and see every field

Then finish the merge and push:
```
git add entity/task.py ui/cli.py
git commit -m "Merge main into round2-X"
git push
```
Your PR updates automatically and should now say *no conflicts*. Merge it on GitHub.

> Stuck and want to start over? `git merge --abort` puts your branch back exactly as it was before `git merge main`.

**Person A** (3-person groups): repeat 2.3 after C's PR is merged.

### 2.4 Verify (whoever merged last)
Pull `main`, run the tests, run the program. Everyone should see all fields in the task list.

---

## Round 3: Your own code, your own conflict (less guidance)

**The story:** Each of you implements a new menu option. The product owner wants every new feature **as option 5**, with **Quit moved to option 6**. You'll soon find that you can't all be option 5.

| Role | Ticket |
|---|---|
| **A** | **Clear completed tasks.** Option 5 removes every completed task and prints how many were removed. |
| **B** | **Edit a task.** Option 5 asks for a task ID and a new description, and updates the task. Print a helpful message if the ID doesn't exist. |
| **C** | **Show pending tasks.** Option 5 lists only the tasks that are not completed. |

Requirements for every ticket:
* Add your option as `5.` in `_print_menu`, and change Quit to `6.`
* Add a matching `elif` in `run()`
* Put your handler method (e.g. `_handle_clear_completed`) **directly after** `_handle_delete` in `ui/cli.py`
* Keep it small; 10 to 15 lines of code is plenty. (Adding a new use case in `use_cases/` is great design but optional today.)

**Merge order: C → A → B** (2-person groups: A → B)

Do the full workflow yourself: update `main`, branch (`round3-X`), implement, test, commit, push, PR, merge in order, and resolve any conflict **locally** as in Round 2.

**Definition of done** (whoever merges last checks these on `main`):
- The menu lists every feature exactly once, numbered 1, 2, 3, … with **Quit last**
- Each number in the menu runs the right feature in `run()`
- All handler methods are present, and none were lost in the merge
- `python -m unittest` passes and every menu option works in `python main.py`

*Think about it:* choosing "ours" or "theirs" wasn't enough here. What did the correct resolution require that neither version had?

---

## Round 4: The conflict Git can't see

Update `main`. Person A: branch `round4-a` and apply `rounds/round4/A.patch`. Person B: branch `round4-b` and apply `rounds/round4/B.patch`. Read your own diff, commit, push, and open PRs. Merge A, then B. (C: you're the tester. When both are merged, pull `main` and run everything.)

Did Git report a conflict? Now run `python -m unittest` on `main`. Figure out what went wrong, why Git didn't catch it, and fix it on a new branch with a PR.

