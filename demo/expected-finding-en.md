# Expected finding for rehearsal — NOT an actual AI review

This file is instructor-authored preparation. No CodeRabbit run has been performed locally. A real reviewer can miss the bug, report it differently, or report additional findings.

The `demo/review-bug` branch rounds the payable amount instead of rounding the discount first. For subtotal 50.05 and STUDENT10, the unrounded discount is 5.005. The contract requires discount 5.01 and payable 45.04. The buggy implementation produces 45.05. The changed return/calculation lines are the relevant code location; inspect the current PR diff for actual line numbers.

Local acceptance should reject the candidate. Reference and repaired candidates should pass 27/27. This is a known seeded fault, not evidence about a model's general detection rate.

The PR extracts named pricing constants. Its repair keeps that useful refactor while restoring discount-first rounding, so the final diff is meaningful rather than an empty revert. The starting `main` in the instructor demo is correct. The student lab's starting `main` is deliberately faulty. Use separate GitHub repositories to keep those two lessons distinct.
