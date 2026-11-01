# Critical decision playbooks

The manager chooses applicable strategies and records concise decisions. These are failure-pattern prompts, not compulsory infrastructure or universal technology choices. Validate the owning source before prescribing project-specific APIs or policies.

## State, UI and asynchronous work

Specify one source of truth, committed state versus temporary edits, valid transitions and terminal meanings. Bind async results to immutable input identity/generation. Editing invalidates dependent eligibility immediately. A late response cannot override newer intent; disposal stops updates. Cancellation must restore committed state and focus/scroll where relevant. Define optimistic UI only with a concrete rejection/reconciliation path.

Decide what survives navigation, restart, upgrade and environment change. Do not confuse memory mutation, cache update and durable persistence. Keep environment/user/tenant ownership explicit. For a branch/service/address change, define the entire transaction and cart/data-loss consent before individual widgets implement pieces of it.

## Money, idempotency and external side effects

Keep amounts in defined minor units and server-owned quotes/eligibility. Persist operation identity and required recovery material before a charge-capable mutation. Reuse identity for uncertain outcomes; timeout is not refusal. Persist returned access/result before clearing recovery context or user input. Distinguish transport retry, business retry and deliberate new operation.

Specify duplicate/out-of-order callbacks, signature/amount/currency/reference validation, provider status reconciliation, refund/fulfillment independence, ledger uniqueness and authoritative success. A browser return is not payment proof. Use approved compensating actions rather than claiming a database revert reverses an external charge. Document behavior after retention/TTL expiry and before a new attempt is allowed.

## Concurrency, jobs and retries

Define invariant and ownership at the actual contention boundary: unique constraints, transaction/lock scope, lease/version checks, queue deduplication or idempotent handlers. A process-local boolean does not protect multiple workers/servers. Model concurrent requests, expiration, crash while owning a lock and replay after partial success.

Use bounded timeout/backoff and one retry owner. Honor server retry deadlines through timer, manual and resume paths; prevent overlapping requests. Bound poison-message retries and expose dead-letter/recovery ownership. Decide how stale UI is labelled and how old/new workers coexist during rollout.

## API, schema and event compatibility

Record method/path, auth, ownership, schema, money/time/ID semantics, status/error codes, pagination, rate limits, timeout and idempotency. Separate syntactic success from domain success. Validate server-side and type/parse consumer-side; unknown fields/states must have deliberate behavior. Use shared contract fixtures without erasing independent producer/consumer checks.

Document compatibility window and deprecation. Avoid breaking old clients with renamed/removed fields, new required data or changed semantics. Version only when needed; do not add an abstraction or service merely to look architecturally sophisticated.

## Data migration, backfill and rollback

Identify data owner, volume, constraints, lock budget, supported old/new code and recovery point. Prefer expand -> compatible code -> resumable bounded backfill -> verify -> contract after the compatibility window. Define null/default semantics, uniqueness, duplicate cleanup, resume markers and verification counts/reconciliation.

Distinguish code rollback from data rollback. Some changes require roll-forward or restoration instead of a reversible migration. Specify protected backup and tested restore where impact warrants it; a backup command without a restore path is weak proof. Never prescribe destructive migration or database reset as a routine way to pass tests.

## Authentication, authorization and privacy

Map actors to permitted resources/actions, including tenant/branch scope and server-side ownership. Test authenticated but unauthorized access, ID guessing, privilege transitions, revocation, token expiry, recovery and session rotation. Do not trust client roles, hidden buttons, QR strings or CORS as authorization.

Minimize collected data; define retention/deletion/export, sensitive-log redaction, secrets storage and test-data isolation. Keep interactive credential handling consistent with the environment's credential-management rules. Do not emit raw secrets in reports, screenshots or fixtures. Missing security requirements should become explicit decisions, not an unbounded security program.

## Dependencies, builds and performance

Prefer existing capabilities before adding dependencies. Record reason, compatibility, lockfile changes, provenance/licensing and native/build impact. Pin reproducible inputs for the candidate; do not silently upgrade the whole stack or execute an unknown install script. Verify actual installed tool interfaces instead of inventing flags.

Set budgets around a real journey: p95 latency, startup, frame/render time, memory, bundle size, query count, load or cost. Measure before/after under a comparable environment/data set. Test the plausible hot path and resource leak; do not substitute a microbenchmark for the actual bottleneck. Avoid an arbitrary performance target presented as an owner requirement.

## Deployment, feature flags and operations

Decide environment parity, configuration source, progressive exposure and compatibility ordering across app/server/schema/workers. A flag needs safe default, owner, targeting, observation and retirement; it is not proof the code works. Define release-readiness separately from release authorization.

Specify health/user/business metrics, correlation IDs, alert owner, observation window and stop/rollback thresholds. Include restore/reconciliation when code rollback cannot restore state. Keep known-good artifacts and production proof separate from local simulation. Do not create monitors, send notifications or deploy simply because the plan mentions them.

## Decision record format

Use `DEC-ID | problem/invariant | chosen behavior | concise rationale | material alternative rejected | evidence/assumption | owner | revisit trigger`. Record decisions that affect correctness, compatibility, security or acceptance. Leave routine helper naming and equivalent local implementations to developers.
