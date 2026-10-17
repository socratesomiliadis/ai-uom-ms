# AI software engineering lecture and lab

A 60-minute lecture for Software Engineering Master's students familiar with Java and Jenkins. Teaching materials are Greek; AI prompts are English. The lesson follows a ticket through implementation, automated evaluation, review and merge, then explains further pipeline automation.

## Where to work

| Path | Contents |
| --- | --- |
| `outputs/` | Current presentation, instructor guide, student lab, prompts, speaker notes, rehearsal script, professor proposal and email draft |
| `ai-production-lab/` | Student repository source: Java, Maven Wrapper, tests, evaluator, GitHub Actions and Jenkinsfile |
| `instructor-assets/` | Reference solution, five seeded faults and recorded local verification results in JSON |
| `source/html-deck/build_html.py` | HTML presentation layout, styling and interaction code |
| `source/html-deck/fonts.json` and font files | Embedded Greek-compatible fonts and their licenses |
| `source/deck-content.json` | Slide metadata, timing, speaker notes and sources |
| `source/prompts.json` | Structured English prompt source |
| `tools/create_proposal.py` | Builds `build/proposal.html` and writes the email draft |
| `tools/package.py` | Rebuilds the four ZIP distribution files in `outputs/` |
| `demo/` | CodeRabbit configuration, English prompts, PR body, handwritten bug/fix fixtures and local verification JSON |
| `tools/prepare_review_demo.py` | Builds an independent Git demo repository with three branches and a portable bundle |
| `outputs/github-demo-setup-el.md` | Exact GitHub publishing, app installation, protection and rehearsal steps |

This is the standalone project in `D:\Projects\Lectures\ai-uom-ms`. The parent `Lectures` directory can hold other lecture projects. Codex scratch files, installed dependencies, build logs and previous Git metadata were excluded from the move.

Start with `outputs/START-HERE-el.md` and `outputs/readiness-check-el.md`. Open `outputs/ai-production-lecture-el.html` directly in a browser; no server or installation is required to present it.

## Making changes

Edit the Java lab under `ai-production-lab/`. Edit the guides and rehearsal script in `outputs/`. For slides, edit layout and visible text in `source/html-deck/build_html.py`, and the corresponding notes and timing in `source/deck-content.json`, then run from this repository root:

```sh
python source/html-deck/build_html.py
```

Keep `outputs/deck-speaker-notes-el.md` consistent with the slide notes. When changing a prompt, also update its copies in the lab, teaching guides and `source/prompts.json`. Regenerate the PDFs and ZIP distributions after relevant content changes; they do not update automatically. The HTML's print function can export the slide deck as PDF with backgrounds enabled. To regenerate the ZIP files, run `python tools/package.py`.

Use ordinary Git commands to inspect and save changes:

```sh
git status
git diff
git add <changed-paths>
git commit -m "Describe the change"
git log --oneline
```

Build outputs, caches, credentials and ZIP distributions are ignored. PDFs, the standalone HTML and the preview image are tracked as reviewable teaching deliverables.

## Running the lab locally

From `ai-production-lab/`, run:

```sh
python ci/evaluate.py --candidate . --trusted . --mode legacy --out reports/legacy
python ci/evaluate.py --candidate . --trusted . --mode acceptance --out reports/acceptance
```

The starter is deliberately faulty: legacy tests pass, while full acceptance has five failures in 27 tests. The instructor reference passes 27/27. Java and Python must be available; the Maven Wrapper downloads Maven and dependencies on its first run. Full setup instructions are in the lab README and instructor guide.

## Publishing the student lab

This is the complete authoring repository, including instructor solutions. Publish only the contents of `ai-production-lab/` as a separate student repository, without its ignored build folders. The student workflows expect those files at the root of that repository. They intentionally do not run as root workflows in this authoring repository.

Before teaching, provision the GitHub repositories, configure permissions and branch protection, and complete a live CI and AI review rehearsal using `outputs/github-demo-setup-el.md`. Recorded results are local verification evidence, not a claim that a hosted classroom environment already exists. No Git remote is configured by this setup.

## Free instructor AI review demo

The four-minute demo occupies minutes 48–52, within the 60-minute lecture. A separate public demo repo has a correct `main`, a constants-refactor PR with a seeded rounding bug, and a prepared repair branch that retains the refactor. CodeRabbit reviews the PR automatically. The instructor validates a finding, passes it to a free implementation chat and commits the fix manually. Actions reruns the evaluator; the final AI PR description uses actual evidence. Autonomous repair and auto-merge remain outside this demo.

The prepared local repo is `build/ai-review-demo`; the portable `outputs/ai-review-demo.bundle` contains all three branches. To regenerate it in a fresh checkout, run `python tools/prepare_review_demo.py`. If that local destination already exists, reuse it or pass `--destination` with a new path; the script never deletes or overwrites an existing repository. Then run `python tools/package.py` for updated distribution ZIPs. The demo bundle and ZIPs are ignored generated artifacts; all their inputs are tracked.

Regenerate speaker notes with `python tools/build_speaker_notes.py`. Optional browser verification and PDF export use Playwright plus an installed Chrome browser. Install Playwright into the ignored project build directory with `npm install --prefix build/browser-tools --no-save playwright`, set `PLAYWRIGHT_MODULE_PATH` to that directory's `node_modules/playwright`, then run `node tools/check_deck.cjs` or `node tools/export_pdfs.cjs`. Run `python tools/create_proposal.py` before exporting its PDF. `CHROME_PATH` can select an explicit Chrome executable; otherwise the scripts use Playwright's Chrome channel. `node tools/update_preview.cjs` rebuilds the preview from screenshots generated by the browser check.

For optional local verification, install `PyYAML` and `jsonschema` into `build/verification-deps` and run `python tools/verify_review_demo.py`. It validates the CodeRabbit config against the published schema, checks correct/bug/fixed candidates and records actual JSON results in `demo/verified-results/`. It requires Java, Python, Git and network access for schema/Maven downloads, and does not call any AI service. The local demo repo must exist first.

Complete `outputs/demo-run-record-el.md` after the real GitHub rehearsal. The expected finding is labeled instructor-authored preparation. No actual CodeRabbit output or live GitHub result is fabricated or bundled. CodeRabbit's current public-repository free offer and setup sources are linked in the setup guide; check them before teaching.
