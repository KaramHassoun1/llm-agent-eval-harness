---
name: error-analysis
description: Classify every failure in an eval results file as agent bug, dataset bug or judge bug, and log findings in docs/EXPERIMENTS.md.
argument-hint: "[results/<file>.json]"
disable-model-invocation: true
---

Analyse the failures in `$0` (default: the newest file in `results/`).

1. Delegate the reading to the `failure-analyst` subagent: give it the results path and ask for a
   table with case_id | metric | category | label (agent bug / dataset bug / judge bug / flaky) |
   one-line evidence (quote the tool call, the policy rule or the judge reason).
2. Check its "dataset bug" and "judge bug" labels yourself against `policy.py` and the case YAML.
   Those labels are the easiest to get wrong, and they decide whether we change the agent or the test.
3. Group the failures into at most 5 root causes, ranked by number of cases affected.
4. Append a dated section to `docs/EXPERIMENTS.md`: run label and file, headline numbers,
   root-cause table, and one proposed change per root cause with the metric it should move.
5. Stop. Don't implement any change. I'll pick which hypothesis to test next.
