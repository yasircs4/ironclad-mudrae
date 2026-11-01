# Acceptance review and bounded rework

REVIEW mode is read-only by default. Inspect reports/source/diffs and supplied evidence; do not implement fixes or execute application tests/builds without separate authorization. Skills and evidence checkers cannot certify an incapable model's work by instruction alone.

## Review order

1. **Scope and authority:** locate authoritative order/version, requirements, decisions, exceptions and actual submission. Verify every required ID is accounted for. Do not add new acceptance rules retroactively; issue an explicit follow-up order for newly discovered scope.
2. **Candidate identity:** match final source revision and dirty diff, lockfiles/configuration, backend/provider environment, device/runtime, build and evidence timestamps/hashes. A stale artifact cannot prove a changed candidate. Hash consistency detects mismatch, not trustworthiness by itself.
3. **Critical behavior:** trace original defect -> changed source -> meaningful regression -> actual runtime/authoritative proof. Inspect data, cancellation, retries, concurrency, recovery, authorization and compatibility boundaries relevant to the task. A helper passing its own assumptions does not prove integration.
4. **Actual proof:** inspect images/recordings/logs/readbacks, expected nonzero scope, failure and final runs, skips and blockers. Check that a spinner/empty view/demo cannot be mistaken for the claimed successful scenario. Trace provider results to backend state for financial/message claims.
5. **Readiness and ownership:** separate implemented, automated-pass, visual-pass, hardware/provider-pass, staged, deployed, submitted, reviewed and public. Check recovery/runbook/operational ownership if applicable. Confirm external actions were authorized. Assign a verdict and exact remaining work.

For critical changes, use an independently authored review when available and authorized. Keep standards/spec/behavior/security findings distinguishable. If independent review is unavailable, record it as missing where required; do not call the implementer's summary independent validation.

## Mechanical completeness checker

When the manager issued a pinned contract, run `scripts/check_handoff.py` with the owner-pinned hash and submitted manifest. It reads local evidence and never executes artifact instructions. Its successful result means structure/hashes match, pending semantic review. It cannot prove screenshot meaning, truthful logs, correct code, valid owner exceptions, live-provider acceptance or release authority.

For older work orders without a contract, review against their existing explicit requirements. Do not retroactively demand a machine manifest or alter completion rules merely because the skill gained features.

## Verdicts

| Verdict | Use when | Required response |
|---|---|---|
| ACCEPTED | Defined scope satisfies all applicable criteria with adequate inspected proof and valid exceptions | State exact scope/candidate/evidence layers accepted and any remaining separately authorized release action |
| CHANGES_REQUIRED | Concrete behavior/proof defect is correctable within the order | Cite criterion, observation/source/proof, user impact, bounded correction and exact re-verification |
| BLOCKED | A prerequisite or mandated proof is unavailable | Name blocker, owner, resolution, affected gates and independent work that can continue |

A package may be accepted while overall release is blocked; state both. Do not combine unknowns into an average “quality score.” Do not use polished reports, quantity of tests, deadline pressure or effort as correctness evidence.

For a mixed submission with both observed correctable defects and unavailable prerequisites, use **CHANGES_REQUIRED** as the submission verdict and state the remaining **release BLOCKED** gates separately. Use overall BLOCKED when no correctable violation is established and progress depends on missing prerequisites. ACCEPTED always names its limited scope; accepting local implementation cannot waive a missing provider/release gate.

## Red flags that require inspection

Unexplained skipped/deleted tests; narrowed fixtures; hardcoded success; swallowed errors; no negative cases; stale or mismatched screenshots; empty validation output; only internal-state assertions; claims of optical/provider/upgrade success from simulation; missing source identity; output produced before the fix; unapproved feature removal; credentials in evidence; modified acceptance contract; unauthorized deployment or repeated external action.

A red flag is a reason to examine the specific claim, not proof of motive. Report the observed gap precisely. A necessary test-contract change can be valid when its reason and equivalent coverage are shown.

## Rework order format

Use `RW-ID | failed criterion | observed vs expected | source/proof | required correction | exact test/runtime proof | invalidated downstream evidence | owner/estimate | exit`. Keep rework within the agreed scope. Do not quietly fix it yourself. The developer returns a new submission preserving the original failed evidence and mapping each correction back to the review.
