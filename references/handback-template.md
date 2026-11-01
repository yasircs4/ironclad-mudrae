# Required developer handback

The work order sets an exact output directory and filename set. Use these defaults if the order does not name an existing project convention:

```text
<absolute-project-path>/planning/handbacks/<work-order-id>/<submission-id>/
  REPORT.md
  REQUIREMENTS.md
  VALIDATION.md
  RISKS.md
  evidence/INDEX.md
  evidence/logs/
  evidence/screenshots/
  evidence/recordings/
```

Create evidence subdirectories only when used. A new submission preserves prior failure evidence and points to superseded evidence rather than overwriting it.

## REPORT.md

Include work-order/version, submitted verdict, executor names/roles, date/timezone, absolute source paths, start/final revision, dirty diff identity, changed-file inventory and artifact hashes. Explain actual behavior changed and critical decisions followed. Distinguish implementation, automated tests, visual review, physical/provider proof, deployment and store/public state. State exact actions not performed. Link all package reports if the work order requires them.

Report applicable lifecycle gate results and any changed assumptions/decisions with their authority. Include dependency/lockfile/configuration changes and the actual supported compatibility matrix when affected. Do not describe unaudited changes as a clean candidate merely because a commit hash exists.

## REQUIREMENTS.md

One row for every requirement, defect and acceptance criterion:

| ID | Required outcome | Changed file/line | Test/case | Runtime proof | Result | Gap or exception authority |
|---|---|---|---|---|---|---|

Use PASS, FAIL, BLOCKED or OWNER_ACCEPTED_EXCEPTION. A final NOT_RUN row prevents acceptance. No row may be silently omitted. Quote the owner's explicit exception source when applicable.

If a pinned machine contract was issued, return `handoff-manifest.json`, the unchanged contract reference/hash and checker JSON output. Its verdict is structural only. Map all manual/provider/visual requirements too; do not silently omit criteria that the checker cannot semantically inspect.

## VALIDATION.md

For each command/run record working directory, command, start/end timestamp, exit code, expected coverage, observed coverage and original log path. Keep initial failures and final reruns. Identify platform/device/OS, locale, theme/text scale, backend/provider mode and source/artifact revision. Explain precisely what a mocked/unit/simulator run proves and which gate it cannot satisfy.

Record skipped/quarantined cases, baseline failures, fault-injection setup and meaningful before/after regression evidence. Identify affected proof rerun after the last material change. A log excerpt must link its original file; a hand-written summary is not original execution output.

## RISKS.md

Record unresolved in-scope issues, external blockers and separately identified out-of-scope risks. Each needs severity, reproduction/evidence, user/business impact, owner role, safe continuation boundary and specific resolution. Report no unresolved risks explicitly when true; do not hide incomplete work under that phrase.

## evidence/INDEX.md

Link original logs, screenshots, recordings and redacted provider/deployment readbacks. For every item state criterion/case ID, capture time, source revision/build hash, environment, device/viewport/locale, route/state and observation. Identify what the evidence does and does not prove.

Require actual rendered screenshots for every applicable UI outcome and its important alternate states. A filename, loading screen or empty state cannot prove a camera scan, populated dashboard, completed payment or successful address lookup. A screenshot cannot by itself prove durable storage, idempotency or financial settlement. Supply the additional readback/recording required by the plan.

## Conditional engineering and operational artifacts

Only require artifacts that the work order made applicable: API/schema/error contracts, decision records, migration/backfill/restore reconciliation, security/tenant evidence, measured performance comparison, CI/check links, signed build/deployment identity, store/target readback, rollout observation, rollback/compensation and support runbook. Put them in existing project documentation where appropriate and link exact paths.

For long work, include the resumable execution ledger and package reports. For a release, name the actual operating owner, monitoring thresholds, observation result and unresolved follow-up. A plan or prepared runbook is not proof of deployment or incident recovery.
