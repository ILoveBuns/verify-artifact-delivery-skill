# Submission evidence

Verified on 2026-08-09.

## Kaggle publication

- Competition: `skill-lift`; official API deadline: 2026-08-13 06:55 UTC.
- Submission mechanism: Kaggle Hackathon Writeup, not a leaderboard file.
- Hackathon writeup ID: `82066`; writeup/project ID: `107555`.
- State: `PUBLISHED`; track ID `596` (`Static Skills`).
- Published URL: <https://www.kaggle.com/competitions/skill-lift/writeups/verify-artifact-delivery-a-safety-first-handoff>
- Published attachment: `benchflow-skill-lift-submission.zip`, 4,782 bytes.
- The attachment was updated through the authenticated Kaggle Writeup editor,
  then downloaded again from the new public storage object on 2026-08-09 and compared
  byte-for-byte with the locally rebuilt package. Both have SHA-256
  `f31abdbaf3fbae9a1727b72398623ba4c0343d045537902c47cb9046b5d12236`.
- The Kaggle API reports the writeup license as CC BY 4.0. The linked source
  repository and runtime skill remain MIT licensed under the repository
  `LICENSE` file.

The Static Skills track advertises monetary prizes of $5,000, $3,000 and
$2,000 for first through third place. These are possible awards, not earnings
or evidence of selection.

## Published runtime package

- File: `dist/benchflow-skill-lift-submission.zip`
- SHA-256: `f31abdbaf3fbae9a1727b72398623ba4c0343d045537902c47cb9046b5d12236`
- Archive test: passed with no compressed-data errors.
- Contents: `SKILL.md` and `scripts/inspect_artifact.py` under the expected
  `skills/verify-artifact-delivery/` path.
- Inspector regression suite: 14/14 passed. Coverage includes a safe archive,
  parent and Windows-drive path traversal, ZIP symlinks, a high-ratio compressed
  member, exact duplicate names, normalized or case-folded portable aliases,
  Unix special files, excessive archive member counts, Windows-forbidden or
  control characters, repeated separators, and trailing spaces or periods.
- The inspector rejects unsafe paths, links, Unix special files, encrypted members, individual
  oversized members, suspicious compression ratios, oversized expanded
  archives, and excessive member counts before handoff. CRC validation runs
  for metadata-safe archives only, so already-rejected ZIP bombs are never
  inflated merely to confirm that they are unsafe.

## Metadata-first CRC hardening publication

Verified locally and from the public Kaggle attachment on 2026-08-09.

- Source merge: `7130e57`; hardening PR #9 is merged.
- Candidate file: `dist/benchflow-skill-lift-submission.zip`
- Candidate SHA-256:
  `f31abdbaf3fbae9a1727b72398623ba4c0343d045537902c47cb9046b5d12236`
- Size: 4,782 bytes; runtime contents remain limited to `SKILL.md` and
  `scripts/inspect_artifact.py`.
- Inspector regression suite: 14/14 passed locally. GitHub Actions run
  `31323800550` passed independently on Python 3.11, 3.12, and 3.13.
- New fail-closed checks reject Windows-forbidden and control characters,
  repeated separators, and trailing spaces or periods even without a colliding
  alias. A mocked regression proves high-ratio archives are rejected from
  metadata without calling `ZipFile.testzip()`; safe archives still receive
  the CRC test.
- Kaggle remained `Submitted!` after the update. Public storage object `48745`
  downloaded as 4,782 bytes, passed `unzip -t`, and was byte-for-byte identical
  to the local reproducible package at the SHA-256 above.

## Special-file and member-count hardening publication

Verified locally and from the public Kaggle attachment on 2026-08-09.

- Source commit: `c1a3bde`; hardening PR #7 is merged.
- Candidate file: `dist/benchflow-skill-lift-submission.zip`
- Candidate SHA-256:
  `d59f6e046c41e84ae065b32f8c0c51f869d5666c4d476551f9b877f2f3a7d970`
- Size: 4,373 bytes; runtime contents remain limited to `SKILL.md` and
  `scripts/inspect_artifact.py`.
- Inspector regression suite: 12/12 passed locally. GitHub Actions run
  `31321983159` passed independently on Python 3.11, 3.12, and 3.13.
- New fail-closed checks reject FIFO, character/block device, socket, and other
  Unix special-file members, as well as archives exceeding 10,000 members.
- Kaggle remained `Submitted!` after the update. Public storage object `48744`
  downloaded as 4,373 bytes, passed `unzip -t`, and was byte-for-byte identical
  to the local reproducible package at the SHA-256 above.

## Portable extraction hardening publication

Verified locally and from the public Kaggle attachment on 2026-08-10.

- Candidate file: `dist/benchflow-skill-lift-submission.zip`
- Candidate SHA-256:
  `9ed50c30058c9fd3b7cff067e65ea7ff5ee711c770c34a28b94b7c5f38767038`
- Size: 4,201 bytes; runtime contents remain limited to `SKILL.md` and
  `scripts/inspect_artifact.py`.
- Inspector regression suite: 10/10 passed.
- New regression coverage rejects Unicode NFC/NFD aliases, names that collide
  when Windows strips trailing spaces or periods, reserved Windows device
  names, and NTFS alternate-data-stream syntax.
- The package passed its own structural inspector and `unzip -t`, with no
  unsafe, linked, encrypted, ambiguous, suspicious, oversized, or CRC-failing
  members.
- Kaggle remained `Submitted!` after the update, with the deadline displayed as
  2026-08-13 14:55 GMT+8. The public attachment URL changed to storage object
  `48737`; an independent download was 4,201 bytes and byte-for-byte identical
  to the local reproducible package at the SHA-256 above.

The package intentionally excludes authoring-only agent metadata, evaluation
fixtures, bytecode, and caches. This keeps the submitted runtime surface small
and prevents the eval answers from leaking into the skill package.

## Archive-alias hardening publication

Verified locally and remotely on 2026-08-09.

- Candidate file: `dist/benchflow-skill-lift-submission.zip`
- Candidate SHA-256:
  `775ba856eb040ec2bd1d24e7048f024396ba09d850f0946df08123c822ccc0dd`
- Size: 3,840 bytes; runtime contents remain limited to `SKILL.md` and
  `scripts/inspect_artifact.py`.
- Inspector regression suite: 8/8 passed, including exact duplicate member
  names and normalized or case-folded portable-path aliases.
- Archive inspection found no unsafe, linked, encrypted, ambiguous,
  suspicious, or CRC-failing members.

The public Kaggle download is 3,840 bytes, passed `unzip -t`, and is byte-for-byte
identical to the local artifact. The Writeup remains `Submitted!`, retains the
Static Skills track, and its visible evidence now states 8/8 tests, Actions run
`31269954172`, and the new checksum.

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
