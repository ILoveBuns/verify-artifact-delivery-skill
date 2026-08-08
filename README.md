# Verify Artifact Delivery — BenchFlow Skill Lift

[![verify submission](https://github.com/ILoveBuns/verify-artifact-delivery-skill/actions/workflows/verify.yml/badge.svg)](https://github.com/ILoveBuns/verify-artifact-delivery-skill/actions/workflows/verify.yml)

An agent skill that prevents a common failure mode: claiming a file is ready
before confirming that the delivered artifact is structurally valid, safe to
open, and present at the exact handoff path.

## What the skill adds

- A risk-based verification ladder for documents, archives, images and media.
- An archive inspector that rejects path traversal, links and suspicious
  compression ratios.
- Explicit handling for narrow edits: verify both the requested change and
  preservation of unrelated content.
- A concise final handoff contract with path, format and verification result.

## Layout

```text
skills/verify-artifact-delivery/
├── SKILL.md
├── agents/openai.yaml
├── evals/evals.json
└── scripts/inspect_artifact.py
```

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 skills/verify-artifact-delivery/scripts/inspect_artifact.py release.zip
python3 package_submission.py
python3 evals/run_local_ablation.py --model gpt-5.6-terra
```

The eval suite includes a safe archive, a malicious traversal archive, a
document report, a narrow presentation edit, and a negative control where no
artifact is requested.

## BenchFlow status

BenchFlow generated the with-skill and baseline jobs successfully. Execution
cannot complete in this fnOS bridge container because the BenchFlow runtime
requires Docker and the container intentionally has no Docker socket. This
environment limitation is documented rather than represented as an evaluation
result.

See [SUBMISSION_EVIDENCE.md](SUBMISSION_EVIDENCE.md) for the package checksum,
archive validation result, exact runtime contents, and evaluation boundary.
See [EVALUATION_RESULTS.md](EVALUATION_RESULTS.md) for the reproducible local
ablation: 5/6 baseline versus 6/6 with-skill on `gpt-5.6-terra`, plus a 6/6
versus 6/6 frontier-model ceiling run. These are not presented as official
Docker/Daytona BenchFlow scores.
