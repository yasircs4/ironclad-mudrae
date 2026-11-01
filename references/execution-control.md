# Execution control, delegation and recovery

Use to write developer packets or govern authorized execution. It does not turn the manager into an implementer or authorize spawning/messaging other agents.

## A work packet that survives a weaker executor

Give one bounded behavior per packet with: absolute source paths/revision; relevant requirements/decisions only; affected components and interfaces; entry prerequisites; exact changes/invariants; positive/negative/failure cases; known commands; required proof; output paths; time estimate; stop conditions; next dependency. State what must not change. Do not require the executor to rediscover the project or choose the missing architecture.

Use short feedback loops: prove one risky seam, integrate, verify, then expand. Provide concrete examples for subtle contracts, not pages of generic “best practice.” If a model cannot reliably handle the packet, reduce its scope and assign high-risk decisions/review to a capable owner. Never lower acceptance to fit model capability.

## Delegation and shared-state ownership

Delegate only when authorized. Partition independent read-only review or disjoint implementation with explicit ownership and integration order. Shared database/schema/configuration files need one owner. Avoid concurrent edits to the same worktree paths. Use an existing suitable checkout or isolated worktree according to project rules; never reset someone else's changes to simplify integration.

Agent reports are claims until source/diff/proof is inspected. A coordinator request does not grant human authorization for messages or external actions. Do not create user-owned chats for subtasks unless requested. Keep parallelism proportional to useful independent work and resource limits; no duplicate broad agents or idle busy polling.

## Progress and context ledger

Maintain `work-order version, package, actual revision/diff, decisions, completed criteria with evidence, current hypothesis, blockers, next bounded action`. Update at package boundaries and before handoff/context loss. Preserve a failed attempt's evidence and reason; do not reset context into a false clean slate.

On resume, read the ledger and current source state, reconcile new owner instructions, then continue unfinished work. Do not replay completed provider actions or discard unresolved mutation identities. If another developer changed an interface, reconcile the contract explicitly before generating final proof.

## Bounded diagnosis

1. State expected versus observed behavior and reproduce with the smallest representative setup.
2. Collect relevant logs/state/call path and distinguish cause from symptom. Classify implementation, environment, data, provider or test-harness failure.
3. Form one falsifiable hypothesis and define the observation that would disprove it.
4. Apply the smallest justified correction, then verify the original failure and adjacent regression surface.
5. After three failed fixes on the same path, stop that path. Report the doubtful assumption, attempts, observations and exact missing fact/capability. Continue independent permitted work.

Do not patch multiple unrelated guesses, hide an exception, add arbitrary sleeps or inflate timeouts to convert a failure into a pass. A test-harness correction must preserve the intended real behavior and show why the old assertion/setup was invalid.

## Tool and capability failures

Inspect actual tool availability/schema/version/help, auth state and target before adapting commands. Prefer purpose-built connected tools or existing project scripts when appropriate. Missing access requires a precise blocker; never invent credentials, APIs, flags or successful results. A safe fallback must prove the same claim or be labelled a weaker evidence class.

Bound retries by consequence. Retry read-only transient retrieval conservatively; do not retry live messages, charges or other irreversible mutations without their prescribed idempotency/reconciliation policy. A timeout can mean the action happened. Check authoritative state before any permitted repeat.

## Scope change and escalation

Distinguish an in-scope defect from unrelated improvement. Resolve or block the former; record the latter separately. A proposed plan change includes requirement IDs, why the current decision fails, impact, minimal alternative and evidence to rerun. Do not use “out of scope” to evade a required failure path.

Escalate genuine unknown business authority, incompatible API/architecture, destructive recovery, missing hardware/provider proof, unresolved security/financial invariant or exhausted diagnosis. Do not escalate routine equivalent helper/code choices or ask the owner to approve the same already authorized work repeatedly.

## Preparing external action

Complete local implementation, proof and recovery preparation before requesting the final required authorization. Present exact candidate/hash, account/environment, intended mutation/batch, user/data impact, observation and stop/recovery plan. Preserve existing authorization; do not invent a new approval requirement for every reversible local step. After an authorized external action, read back the actual target state and report its real evidence level.
