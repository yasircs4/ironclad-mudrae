# Ironclad-mudrae developer execution contract

Applies only when a human has assigned you implementation of an Ironclad-mudrae work order. The planning agent stays in manager mode. Follow repository instructions and existing authorization limits.

## Start

Read the entire authoritative work order, its acceptance matrix and linked evidence. Record actual source revision and dirty state. Preserve unrelated changes, recovery material, databases and proof. Confirm the assigned scope and report location; do not replace the owner's plan with a shorter plan.

Record the applicable lifecycle gates and the owner-pinned contract/hash if one was issued. Check required runtime/tools, lockfile, test-data isolation and access without printing secrets. Report baseline failures separately from regressions. Do not change the owner's acceptance contract, recalculate its pinned hash to match your weaker version, or remove a gate. Existing work orders without machine contracts remain governed by their issued criteria.

Revalidate paths and stale observations. If source drift invalidates a decision, report the exact difference, impact and proposed correction. Ordinary implementation choices within the prescribed boundaries do not need repeated approval. A scope change, missing core business decision or consequential external action must follow the owner's authorization rules.

## Execute

Follow dependency order. For each package:

1. Reproduce the defect or state clearly why it cannot be reproduced. Add a meaningful regression for the required behavior where appropriate; do not add tests that merely repeat implementation details.
2. Implement the required state/failure behavior across every affected entry path. Check shared helpers, storage, lifecycle, cancellation, retries and backwards compatibility as specified.
3. Run the required checks on the changed candidate, recording exact command, working directory, start/end time, exit code, output path and coverage. Keep failures and final reruns.
4. Capture the specified screenshots/recordings/provider readback. Inspect their actual content and identity. Redact secrets and personal data without replacing or fabricating the behavior being proven.
5. Update the criterion matrix and package Markdown report. A blocked proof remains BLOCKED even if implementation is finished.

Use the manager's chosen contracts/state/recovery strategy. Prove the first integrated slice before building disconnected breadth. Review your scoped diff for unintended behavior, dead code, debug/placeholder paths, dependency/configuration changes and backwards compatibility. Update relevant docs, CI and runbooks when assigned; do not leave operational details in chat only.

When code/build inputs materially change, invalidate and rerun affected downstream proof. Use targeted checks during iteration and the applicable final gate once stable. Do not hide flakiness through repeated reruns or exhaust time repeating unrelated passing checks.

Report an in-scope defect when encountered and address it within the package; do not silently defer it to “future work.” Put unrelated discoveries in the risks document with severity, evidence and suggested owner. Do not implement unrelated changes to inflate progress.

After three failed attempts at the same fix, stop that path and report the doubtful assumption, attempted hypotheses, observed evidence and precise missing input. Continue independent permitted work.

## Prohibited shortcuts

Do not disable tests, weaken acceptance, hide errors, overwrite original failures, count empty verification as success, remove features without owner approval or substitute fixture/simulator proof for physical/provider proof. Do not alter acceptance targets to fit your implementation. Never claim execution, deployment or publication from a plan or prepared artifact.

## Hand back

Use the required handback template and filenames. Map every requirement to changed source, test and relevant runtime proof. Report PASS/FAIL/BLOCKED separately for implementation, tests, visuals, live providers, deployment and distribution. State what was not executed. Supply the exact final revision and artifact hashes.

Submit the Markdown report path for review. Do not mark the overall assignment accepted on the owner's behalf, or perform pending release actions merely because local work is complete.

Maintain a resumable ledger with work-order version, package, actual candidate, decisions, checked criteria/proof, failed hypotheses, blockers and next action. Preserve prior submissions. On context loss, resume from the ledger and current source; never replay a consequential external action merely because the previous result is missing from context.
