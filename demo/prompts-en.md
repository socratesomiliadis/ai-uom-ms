# Instructor demo prompts

All instructions to AI tools are English. Provide the actual ticket, final code or diff, reports, and review finding as separate context. The demo PR title and description must also remain English.

## Repair a reviewed finding

```text
Read the supplied ticket, current PriceCalculator.java, actual CI report,
and the review finding. Check whether the finding is valid before changing code.
If valid, choose the implementation and project changes needed to meet the objective.
You may refactor, introduce helpers, update tests, resources, or build configuration.
Preserve the agreed behavior, public API, and intended named pricing constants.
Explain the violated requirement with a concrete expected-versus-actual example.
If the finding is unsupported, explain the missing evidence instead of forcing a fix.
If you have a terminal, rerun the acceptance evaluator and report actual results.
If you cannot run it, write NOT RUN and return each changed file with its path and content.
Do not merge or claim a successful CI run you have not observed.
```

## Final PR description after the fresh run

```text
Write a concise final PR description in English, at most 120 words.
Use the supplied final diff, ticket, real CI reports, and actual review finding as evidence.
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
