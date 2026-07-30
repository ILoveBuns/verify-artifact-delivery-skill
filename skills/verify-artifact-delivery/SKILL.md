---
name: verify-artifact-delivery
description: Inspect and validate a generated or modified file before claiming completion or delivery. Use for documents, spreadsheets, presentations, archives, images, reports, code bundles, and other file artifacts when correctness, format preservation, required contents, or safe handoff matters. Also use when a task asks to create, edit, convert, package, export, or submit a file. Skip for answers that produce no artifact.
---

# Verify Artifact Delivery

Treat successful creation as provisional until the actual output has been inspected.

## Work from explicit acceptance criteria

- Extract the requested path, format, required content, constraints, and destination.
- Inspect the source artifact before editing. Preserve unrelated content and metadata unless the request requires changing them.
- Resolve ambiguity only when it materially changes the artifact; otherwise choose the narrowest reasonable interpretation.

## Validate in layers

1. Confirm that the intended file exists, is non-empty, and has the requested extension.
2. Run `python scripts/inspect_artifact.py <path>` for a structural inventory. Add `--json` when machine-readable evidence helps.
3. Use a format-aware parser or renderer when available. A ZIP container opening successfully does not prove that a DOCX, XLSX, PPTX, EPUB, or archive is semantically correct.
4. Check required text, sheets, slides, files, dimensions, formulas, links, or executable behavior against the request.
5. For visual artifacts, render or open the result and inspect representative pages or frames. Check clipping, overlap, unreadable text, blank output, and unintended changes.
6. Re-open the final saved artifact after all edits. Do not rely on an in-memory object or a command's zero exit status alone.

Scale validation to the risk. A short text export needs a light check; a client-facing report, archive, or executable bundle needs structural, semantic, and visual or runtime checks.

## Correct narrowly

- Fix the observed defect rather than regenerating unrelated parts.
- Keep the original when overwrite was not explicitly requested.
- Do not include secrets, temporary files, caches, credentials, unrelated data, or hidden evaluation material in a deliverable.
- Inspect archive member names for absolute paths or `..` traversal before extraction or handoff.
- Do not weaken validators, graders, security controls, or acceptance criteria to make an artifact appear valid.

## Deliver with evidence

- State the outcome first and identify the actual artifact path.
- Mention only the checks that materially support correctness.
- Distinguish verified properties from unchecked or unavailable validation.
- Claim completion only after the final saved artifact satisfies the acceptance criteria. If a required external upload or submission is unavailable, report the artifact as prepared, not submitted.

