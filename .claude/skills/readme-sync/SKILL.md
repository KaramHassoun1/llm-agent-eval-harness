---
name: readme-sync
description: Audit README.md and docs against the actual code and fix every mismatch (paths, commands, numbers, thresholds, features).
disable-model-invocation: true
---

The README must only describe what the code does.

1. Ask the `docs-verifier` subagent to audit `README.md`, `CLAUDE.md` and `docs/*.md`. It returns a
   list of claims with a verdict (OK / MISMATCH / UNVERIFIABLE) and evidence for each.
2. For each MISMATCH, decide which side is wrong:
   - The doc is stale → fix the doc.
   - The code is missing a feature the roadmap promises → don't describe it as existing; move it
     to a "Roadmap" line or remove it.
3. For numbers (scores, case counts), cite the results file they came from. Remove any number you
   can't trace to a file in `results/`.
4. Re-run the verifier on the changed files and show it reports zero mismatches.
