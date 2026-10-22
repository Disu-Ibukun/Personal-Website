# Publishing a credible technical case study

Your site reads its data from `content/site.json`. The current cryptocurrency pipeline is intentionally unpublished because the brief did not supply architectural facts, tools, or outcomes.

1. Find the corresponding object inside `projects`.
2. Add a factual summary and technology names in `stack` (only tools you actually used).
3. Complete `challenge`, at least one `approach` paragraph, at least one `decisions` entry (each `title` and `body`), `outcomes` and `lessons`.
4. Add `architecture` and `quality` if they are relevant. Add `image_file` only for an actual image in `public/assets/`, e.g. `assets/architecture.png`.
5. Set `published` to `true` and run `python build.py`. The build will reject incomplete case studies and create `/projects/YOUR-SLUG/`.

Example structure for **a decision**, not a claim about your project:

```json
{"title": "[Design choice]", "body": "[What you chose, why, what you gave up]"}
```

Copy the project object and assign a new unique lower-case hyphenated `slug` to create more project pages. Don't publish examples as if they were your own work. See `README.md` for all updates.
