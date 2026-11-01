# Work order authoring structure

Use concrete values from the project. Replace all drafting prompts before delivery. No required decision may remain disguised as “TBD,” “as needed” or “developer to decide.” An external fact may remain explicitly BLOCKED with owner and resolution path.

## Authority and outcome

Record title/ID/date/version, authoritative document path, owner, executor roles, absolute repository/worktree paths, branch/revision, primary specs and existing evidence. State desired user-visible/system behavior and measurable acceptance. Specify exactly which actions the assignment authorizes and which require separate approval.

Classify risk as scoped, standard or critical with reason. List applicable lifecycle gates G0-G11, planned verification owner and any genuinely inapplicable gate with rationale. Separate owner decisions, verified facts, supplied claims and unresolved facts. Set support/compatibility and actual quality budgets; do not invent a coverage percentage or release date as an acceptance target.

Distinguish **DISCOVERY_READY** from **IMPLEMENTATION_READY**. If the user supplies only a feature idea without the actual repository, schema or command facts, issue a bounded discovery package with specific questions and outputs. Do not invent absolute application paths, tests or API names. The dependent implementation is blocked until those facts are supplied and the manager's strategy is validated. The plan can make safe architectural decisions now while documenting unknown business/provider authority.

Example: for “add cancellation/refunds” without repository or refund policy, decide server authority, tenant isolation, durable idempotency and compatibility invariants. Require the actual repository and existing policy at kickoff; keep refund dispatch disabled until policy/provider semantics are confirmed. Do not call the full implementation ready merely because a high-level order was written.

## Fixed decisions and boundaries

State scope/exclusions, platform/locales, compatibility, data/migration rules, persistence/recovery ordering, source-of-truth, user-consent rules and external-action boundaries as applicable. List real unknowns with impact, conservative default and accountable owner. Separate business requirements from implementation preference.

Include concise decision records for consequential architecture/API/schema/auth/concurrency/dependency/recovery choices. Add operational ownership, monitoring and release/rollback strategy when applicable. Define a timeboxed discovery/spike only for a specific unresolved fact; require the resulting decision and a separate production gate. Do not hand the strategy back to the developer as “choose the best approach.”

## Execution packages

For every package include:

| Field | Required content |
|---|---|
| Identity | Stable ID, owner role, dependency, bounded effort estimate |
| Input | Known defects/requirements and current evidence |
| Implementation direction | Concrete changes and owning files/components; manager-made critical decisions |
| Invariants | What must always remain true, including cancellation and failure |
| Verification | Reproduction, positive/negative/interruption cases, exact known commands and runtime environment |
| Proof | Required logs, screenshots, recordings, readback and source/artifact identity |
| Exit | Binary acceptance criteria, status per criterion and next dependency |
| Escalation | Specific blocker conditions and safe continuation boundary |

Add a simple dependency graph/table and first integrated slice. Specify source/build-input changes that invalidate later proof. Assign ownership for shared files/interfaces and integration; parallel execution is optional and requires authorization, not an automatic way to inflate the team.

Provide a complete mapping from every finding/requirement to a package and test. Sequence risky correctness work before dependent UI/capture/release evidence. Include rollback and recovery for consequential state changes without authorizing those changes implicitly.

## Evidence and handback

Specify absolute output directory and required Markdown files. Use the handback template, consistent requirement/case IDs and an evidence index. Require final source revision, changed files, exact commands/exit codes, real runtime proof, unresolved risks, explicit untested boundaries and implementation/deployment/provider/store state.

For new critical/multi-package work, author an acceptance contract with expected criterion IDs, evidence types/case IDs, required reports and target environment. Pin its literal SHA-256 in the order with the exact read-only checker command. The developer returns the manifest but cannot author a weaker replacement contract. Require semantic review after a structural pass. For small work or legacy orders, preserve a proportionate existing acceptance format.

If release/operations are in scope, require candidate freeze, actual configuration/signing identity, compatibility/upgrade/migration proof, restore/rollback or compensating recovery, rollout cohort/metrics/stop conditions, target readback and support/runbook ownership. State which gates can be prepared locally and which need authorized live action.

## Ready-to-send message

Deliver a fenced `text` message that names the absolute repository, authoritative order, dependent specs, execution commands, mandatory package sequence, acceptance rule and final report path. The recipient must be able to start without asking where the code or plan is. Keep the owner's approval/review authority explicit.
