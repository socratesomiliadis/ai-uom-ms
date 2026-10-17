# Instructor demo prompts

All instructions to AI tools are English. Provide the actual ticket, final code or diff, reports, and review finding as separate context. The requested PR description can be Greek.

## Repair a reviewed finding

```text
Read the supplied ticket, current PriceCalculator.java, actual CI report,
and the review finding. Check whether the finding is valid before changing code.
If valid, make the smallest fix to PriceCalculator.java. Preserve the public API
and keep the intended extraction of named pricing constants.
Do not change tests, expected values, the ticket, CI, or dependencies.
Explain the violated requirement with a concrete expected-versus-actual example.
If the finding is unsupported, explain the missing evidence instead of forcing a fix.
If you have a terminal, rerun the acceptance evaluator and report actual results.
If you cannot run it, write NOT RUN and return the complete corrected Java file.
Do not merge or claim a successful CI run you have not observed.
```

## Final PR description after the fresh run

```text
Write a concise final PR description in Greek, at most 120 words.
Use only the supplied final diff, ticket, real CI reports, and actual review finding.
State the behavior restored and why the change is needed.
Include one worked example, the actual final run URL, tested checkout SHA,
and PR head SHA when supplied. Preserve the distinction between these SHAs.
State whether the review finding was reproduced and resolved.
Mention relevant evaluation limits and how to revert the fix commit.
Use NOT RUN or NOT VERIFIED where evidence is absent. Never fabricate evidence.
Link detailed reports instead of pasting logs. Do not merge the PR.
```

## Reviewer fallback in a fresh free chat

Use this only if the CodeRabbit service is unavailable. Announce the change of tool; do not present this output as a CodeRabbit review.

```text
Review the supplied ticket, PR diff, and actual test report as a code reviewer.
For each material finding, identify the code location, violated requirement,
concrete input, expected output, actual output, and supporting evidence.
Label hypotheses. Do not invent executed checks or successful results.
If no finding is supported, say NO VERIFIED BLOCKERS and state what is unchecked.
Do not merge. Keep the response concise.
```
