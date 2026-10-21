---
name: eval-run
description: Run the refund-agent evaluation with a cost check, save results, and compare them to the baseline.
argument-hint: "[label] [--limit N] [--runs N] [--model M]"
disable-model-invocation: true
---

Run an evaluation labelled `$0`. Extra CLI flags from the user: $ARGUMENTS

Last saved runs:
!`git ls-files --others --cached results | tail -n 5`

1. Estimate the cost: number of cases × runs × (agent calls + judge calls). Give a rough token and
   dollar estimate from the last run's metadata if there is one. If it's more than a `--limit 5`
   smoke run, show the estimate and wait for my OK.
2. Run `uv run refund-eval --label $0 <flags>` in the background. Don't stream the full output
   into this conversation; read the saved JSON afterwards.
3. Report a compact table: metric, mean, std, pass rate, pass^k, Δ vs `evals/baseline.json`.
   Then the same per category. Bold any regression greater than 5 points.
4. List failing case IDs grouped by metric (IDs only, no transcripts).
5. Suggest running `/error-analysis <results file>` if there are failures. Don't start fixing anything.
