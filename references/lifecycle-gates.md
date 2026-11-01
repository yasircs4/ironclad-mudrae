# Development lifecycle gates

Use this to design an assignment or review its stage coverage. The manager decides applicable gates and evidence before dispatch. Developers execute only assigned, authorized work. Every applicable gate has an owner, entry inputs, exit criteria, proof and continuation boundary. Gate IDs are stable; work-package IDs are project-specific.

## G0. Outcome, scope and authority

Define the primary user task, business outcome, current failure and desired behavior with concrete examples. Identify actors/roles, exclusions, supported environments/platforms/locales, compatibility and constraints. Separate must-have acceptance from optional improvement. Record work-order version, decision owner, execution permissions and external actions requiring separate authorization.

**Exit:** every known requirement/defect has an ID, observable result and disposition; no critical strategy is left for developers to guess. Open external facts have an owner, safe default and resolution gate. Avoid asking the owner to decide routine implementation details.

## G1. Repository, environment and baseline

Map entry point -> business logic -> storage/provider -> consumer. Record actual repository/worktree, branch/revision, dirty state, applicable guidance, runtime/tool/package-manager versions, lockfiles, build profiles and test commands. Inventory CI, test fixtures, signing/provider/hardware access and source-of-truth documents without exposing secrets. Preserve unrelated changes and recovery assets.

Assign developers baseline checks and reproducible setup steps. Distinguish existing failures from regressions. An unavailable baseline is a known uncertainty, not permission to claim the change passed. A production database, shared test tenant or real SMS account is not a default fixture.

**Exit:** developer can reproduce the environment and initial failure, or a precise environment blocker is documented; source and environment identity are fixed enough to assess later evidence.

## G2. Architecture, contracts and risk

Choose state transitions, ownership, durable boundaries, access rules, concurrency and recovery. Define request/response/event schemas, error meanings, version compatibility and migration sequence. State which changes remain local and which require deployment/provider action. Set relevant latency/resource/accessibility/security budgets from requirements or a measured baseline. Record consequential decisions and revisit triggers.

**Exit:** interfaces and critical invariants are explicit; failure paths are designed; compatibility/rollback are credible; no speculative rewrite or unbounded dependency upgrade is hidden in scope.

## G3. Package sequence and first integrated slice

Split work by verifiable behavior, not disconnected layers that never integrate. Each package owns files/components, dependencies, implementation directions, acceptance cases, evidence, estimate and stop conditions. Start with a thin end-to-end slice proving the riskiest seam, then complete the required breadth. Define a spike separately when a factual uncertainty blocks design; timebox it and require a decision, not production-readiness claims.

**Exit:** the next package can be started without another architecture/planning round; dependencies are ordered and concurrent edits have a single owner. All original requirements map to packages.

## G4. Implementation and developer self-check

Implement all affected entry paths with semantic errors, failure recovery and durable invariants. Keep changes within assigned boundaries; reuse established components and contracts. Avoid swallowing errors, placeholder success, arbitrary delays, magic credentials and unnecessary packages. Update types/configuration/localization as behavior requires. Add meaningful regressions proportionate to impact; do not demand a new test for every reversible cosmetic edit.

**Exit:** the intended behavior is integrated; scoped diff is coherent; configuration and migration implications are recorded; in-scope discoveries are resolved or explicitly blocked. “Compiles” is not behavior verification.

## G5. Automated, contract and runtime validation

Choose tests by failure risk: unit for pure invariants, integration for storage/concurrency/provider boundaries, contract for schemas/errors, widget/browser/native for actual interaction, and physical/provider for real external behavior. Include negative, boundary, cancellation, retry, restart and ordering cases where they can invalidate the outcome. Use controlled clocks and fault injection for timing rather than fragile sleeps.

Run applicable lint/type/static checks, meaningful suites, production build and CI against the final candidate. Capture exact commands and exit codes; check expected cases actually ran. Quarantining a flaky test is an explicit documented limitation with an owner and equivalent coverage decision, not a silent pass.

**Exit:** required coverage executed with candidate identity, or affected criteria remain FAIL/BLOCKED. Mocked or simulator evidence is labelled. No percentage or test count replaces the actual acceptance cases.

## G6. Rendered usability, accessibility and content

For visual flows, specify task success, platform conventions, real content, responsive structure and state hierarchy before craft. Use existing design tokens/components. Require relevant narrow/common/large viewports or native device classes, locales/RTL, text scaling, keyboard/focus/screen readers, supported themes and loading/empty/error/disabled/overlay states. Inspect actual screenshots and interactions. Reference matching must preserve semantics, usability and performance.

For nonvisual work, document why screenshots are inapplicable and require appropriate service/CLI/data proof. Never manufacture a screenshot requirement for an invisible invariant. Mobile store assets use applicable Goldie/release rules and real Release capture, independently of functional QA.

**Exit:** relevant user tasks and alternate states work in the agreed matrix; proof is inspected and current; remaining visual/device gaps are explicit.

## G7. Code, security and integration review

Review behavior against requirements and diff against architecture/standards separately. Trace critical data/error paths beyond the edited line. Inspect authorization, tenant isolation, validation, secrets, dependencies, concurrency, resource behavior and regression risk where relevant. Require a separately authored review for critical changes when authorized and available; otherwise record that independent review is missing. Do not invent a reviewer or approve a self-review as independent.

Resolve actionable findings with a bounded patch and affected verification. Require explanation and evidence for dismissed findings. No approval by tally, report polish or superficial formatting.

Prepare coherent scoped diffs/logical commits and a review description explaining problem, resulting behavior, validation and remaining risk under repository rules and existing authorization. Link requirements and actual CI results. Do not bypass hooks, force-push, merge, or erase unrelated dirty work to obtain a clean-looking review. A draft PR or approved code review is a separate state from a merged/deployed release.

**Exit:** blocking findings closed with proof or owner disposition; final diff and applicable checks are aligned. Review acceptance does not authorize deployment.

## G8. Staging, compatibility and recovery rehearsal

Validate the candidate in the closest isolated runtime, actual API/backend revision, provider sandbox and supported physical hardware where required. Exercise install/upgrade, old/new client/server compatibility, migration/backfill, representative data and worker/queue behavior. Verify financial/provider ledger state independently of frontend displays. Prepare and, when authorized, rehearse rollback/restore or compensating recovery with evidence.

**Exit:** staged behavior and recovery meet the contract; actual device/provider proof exists for required claims; missing access remains blocked. Staging origin alone never proves fake payments or safe notifications.

## G9. Release preparation and authorization

Freeze source, lockfiles, environment profiles, build/signing identities, versioning and artifact hashes. Prepare CI/deployment/store validation, privacy/accessibility/security disclosures, reviewer access, support docs, migration/runbook, monitoring, rollout cohort and rollback thresholds. Match the accepted candidate to the exact action being proposed. Follow existing authorization rather than inventing a universal extra approval ceremony.

**Exit:** all applicable acceptance gates pass or have a recorded owner exception; the exact external action is authorized where required. Local validation, upload, submission, provider review and public availability remain distinct.

## G10. Deploy/rollout and production readback

Only the authorized executor performs the external change. Record actual artifact/config/revision, migration/worker state and deployment result. Use the defined phased rollout/feature flag when needed, with explicit observation window, metric thresholds and stop/rollback criteria. Verify real user-facing and backend state after propagation. Do not infer success from a deployment command or green CI alone.

**Exit:** intended candidate is observed in the intended environment/cohort; health and critical flows satisfy release criteria; rollout/rollback outcome and ownership are explicit.

## G11. Operate, incident response and closure

Provide dashboards/log correlation and alerts tied to user/business failure, with an actual owner and actionable runbook. Record rollback/restore procedures, escalation, unresolved risks and follow-up decisions. For an incident, prioritize containment and preserved evidence; avoid irreversible “cleanup” or financial database edits as a substitute for reconciliation. Authorize any scheduled monitoring separately; a plan does not create an automation.

**Exit:** handback covers all criteria and evidence layers; owner accepts the reviewed scope; operational owner can run/support/recover it. Capture lessons that change future decisions without silently changing global memory or instructions.

## Gate status and evidence reuse

Use PENDING during work, PASS with appropriate proof, FAIL for violated behavior, BLOCKED for missing prerequisites, and OWNER_ACCEPTED_EXCEPTION only with real owner authority. Mark an irrelevant stage NOT_APPLICABLE at planning with rationale. That disposition cannot excuse a required case later.

Carry forward earlier evidence only when candidate, inputs, environment and the verified claim remain valid. After a material change, identify affected downstream gates and rerun those. Do not endlessly repeat passing unrelated tests or reuse stale release evidence after changing build inputs.
