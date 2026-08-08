# Submission evidence

Verified on 2026-08-08.

## Kaggle publication

- Competition: `skill-lift`; official API deadline: 2026-08-13 06:55 UTC.
- Submission mechanism: Kaggle Hackathon Writeup, not a leaderboard file.
- Hackathon writeup ID: `82066`; writeup/project ID: `107555`.
- State: `PUBLISHED`; track ID `596` (`Static Skills`).
- Published URL: <https://www.kaggle.com/competitions/skill-lift/writeups/verify-artifact-delivery-a-safety-first-handoff>
- Published attachment: `benchflow-skill-lift-submission.zip`, 3,561 bytes.
- The attachment was downloaded again from Kaggle on 2026-08-08 and compared
  byte-for-byte with the locally rebuilt package. Both have SHA-256
  `342c2b1e41412dc69fabaac73e6ef3351059010c34b45155f6cd8d68518e41de`.
- The Kaggle API reports the writeup license as CC BY 4.0. The linked source
  repository and runtime skill remain MIT licensed under the repository
  `LICENSE` file.

The Static Skills track advertises monetary prizes of $5,000, $3,000 and
$2,000 for first through third place. These are possible awards, not earnings
or evidence of selection.

## Published runtime package

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

## Archive-alias hardening candidate

Verified locally on 2026-08-09; not yet uploaded to the Kaggle writeup.

- Candidate file: `dist/benchflow-skill-lift-submission.zip`
- Candidate SHA-256:
  `775ba856eb040ec2bd1d24e7048f024396ba09d850f0946df08123c822ccc0dd`
- Size: 3,840 bytes; runtime contents remain limited to `SKILL.md` and
  `scripts/inspect_artifact.py`.
- Inspector regression suite: 8/8 passed, including exact duplicate member
  names and normalized or case-folded portable-path aliases.
- Archive inspection found no unsafe, linked, encrypted, ambiguous,
  suspicious, or CRC-failing members.

This candidate checksum does not replace the published checksum above. The
online attachment remains the 3,561-byte package until a supported update path
is verified and the uploaded bytes are downloaded and compared again.

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
