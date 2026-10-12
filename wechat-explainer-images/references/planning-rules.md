# Visual planning rules

## 1. Decide what deserves an image

Create an image when the section contains at least one of these:

- a core tension or counterintuitive claim;
- three or more components and their roles;
- a process with dependent stages;
- a before/after transformation;
- a comparison whose differences matter;
- safety boundaries or decision criteria.

Do not create a generated image for:

- a transition paragraph;
- a simple list that is already easy to scan;
- a step whose real screenshot is sufficient;
- repeated examples of an idea already visualized.

## 2. Preserve evidence hierarchy

- Generated diagrams explain the mental model.
- Real screenshots prove the workflow and interface state.
- Captions connect the proof to the claim.

Never replace a necessary screenshot with a fabricated interface.

## 3. Plan each asset

Use this compact schema:

| Field | Requirement |
|---|---|
| Filename | Two-digit order plus short ASCII slug |
| Placement | Heading after which the image appears |
| Job | One sentence describing what becomes clearer |
| Title | Short, concrete, and visually dominant |
| Subtitle | One line that resolves ambiguity |
| Labels | Exact strings, usually three to five |
| Takeaway | One concise conclusion or guardrail |
| Visual | Specific objects and reading direction |

## 4. Recommended content patterns

### Tension

Show the apparent solution on the left and the unsolved problem on the right. Use orange for the gap.

### System roles

Place the user's object in the center and arrange three to five role cards around it. Use arrows only when direction matters.

### Process

Use a numbered left-to-right or top-to-bottom pipeline. Give each stage a distinct icon and one short action label.

### Comparison

Use two balanced columns with one axis of contrast per row. Highlight the practical conclusion at the bottom.

### Boundaries

Use a guarded central lane, with allowed actions in blue/green and prohibited shortcuts in orange/red. Keep wording non-alarmist.

## 5. Output location

Prefer a new folder under the article project's existing `assets` area. Name the version clearly, for example `wechat-explainer-v1`. Keep raw generations in a `raw` subfolder and accepted 1080×1440 files at the version root.

