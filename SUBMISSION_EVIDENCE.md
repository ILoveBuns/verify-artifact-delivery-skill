# Submission evidence

Verified on 2026-08-08.

## Runtime package

- File: `dist/benchflow-skill-lift-submission.zip`
- SHA-256: `342c2b1e41412dc69fabaac73e6ef3351059010c34b45155f6cd8d68518e41de`
- Archive test: passed with no compressed-data errors.
- Contents: `SKILL.md` and `scripts/inspect_artifact.py` under the expected
  `skills/verify-artifact-delivery/` path.
- Inspector regression suite: 4/4 passed. Coverage includes a safe archive,
  parent and Windows-drive path traversal, ZIP symlinks, and a high-ratio
  compressed member.
- The inspector rejects unsafe paths, links, encrypted members, individual
  oversized members, suspicious compression ratios, oversized expanded
  archives, and CRC failures before handoff.

The package intentionally excludes authoring-only agent metadata, evaluation
fixtures, bytecode, and caches. This keeps the submitted runtime surface small
and prevents the eval answers from leaking into the skill package.

## Evaluation boundary

BenchFlow generated the with-skill and baseline jobs successfully. Full execution
requires Docker, which is not exposed inside the fnOS bridge container. No score
or lift is claimed from an execution that did not complete.

A separate, explicitly labeled local Codex CLI ablation now provides real
filesystem-backed evidence without claiming to be the official runner. On a
fixed six-case suite, `gpt-5.6-terra` improved from 5/6 baseline to 6/6 with the
skill (+16.7 percentage points); a frontier default run was 6/6 in both
conditions, showing a ceiling rather than invented lift. See
`EVALUATION_RESULTS.md` and the JSON result files under `evals/`.
