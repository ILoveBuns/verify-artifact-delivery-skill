# Submission evidence

Verified on 2026-08-01.

## Runtime package

- File: `dist/benchflow-skill-lift-submission.zip`
- SHA-256: `03e47d68e829503e0ceb1b344e337f17c4bb2f38d18bab2e4ae3e6a0edf92875`
- Archive test: passed with no compressed-data errors.
- Contents: `SKILL.md` and `scripts/inspect_artifact.py` under the expected
  `skills/verify-artifact-delivery/` path.

The package intentionally excludes authoring-only agent metadata, evaluation
fixtures, bytecode, and caches. This keeps the submitted runtime surface small
and prevents the eval answers from leaking into the skill package.

## Evaluation boundary

BenchFlow generated the with-skill and baseline jobs successfully. Full execution
requires Docker, which is not exposed inside the fnOS bridge container. No score
or lift is claimed from an execution that did not complete.
