# Risk-based quality and proof matrix

Select cases that can invalidate this task's required outcome. The manager fixes applicable cases/thresholds before dispatch. A long checklist is not coverage; every case must have an observable expected result, execution method, owner and evidence class.

## Choose the evidence level

| Claim | Appropriate proof | Insufficient substitute |
|---|---|---|
| Pure calculation/normalization/state invariant | Focused unit/property/boundary tests | Screenshot or compiler success |
| API/storage/concurrent operation | Integration/contract test and authoritative state readback | Mock-only consumer test |
| User task/navigation/form/accessibility | Rendered widget/browser/native interaction in agreed matrix | Static component source or a screenshot filename |
| Lifecycle/camera/deep link/device integration | Native runtime and physical hardware where required | Pure helper test or simulated payload |
| Provider payment/message/refund | Approved real/sandbox provider reference plus backend reconciliation | Fake gateway, callback fixture or browser success URL |
| Distribution/deployment/publication | Exact candidate identity and target-system readback | Local artifact, upload command or prepared release notes |

Evidence levels complement one another; none silently upgrades to another. A screenshot can prove displayed content, not persistence, uniqueness or financial settlement.

## Functional dimensions for applicable journeys

Cover normal behavior, minimum/maximum/invalid values, empty/unknown/malformed data, duplicate actions and stale version. Exercise cancel/back, retries after ambiguous failure, reload/restart, changed inputs while requests are pending, response reordering and disposal. Include user roles/tenants/environments and existing data where relevant. Use equivalence classes or pairwise combinations to keep a large matrix bounded, while running critical failure interactions explicitly.

Keep deterministic tests stable through fake clocks, controlled fixtures and observable outcomes. Do not inspect only internal counters or wait briefly when the invariant spans a longer deadline. A regression should fail on the defect and pass on the corrected behavior; provide another valid observation if a historical failing run cannot be reproduced. Never manufacture red-test evidence.

## Web and visual applications

Verify primary task success, semantic controls, keyboard/focus order and restoration, labels/errors, overlays/scroll/safe areas, loading/empty/disabled/error/recovery and network states. Select real narrow/common/large viewports, supported themes, locales/RTL and increased text. Use project accessibility requirements; for web, default to WCAG 2.2 AA where applicable. Automated accessibility checks supplement manual task/keyboard/screen-reader checks.

Inspect actual final renders with real content, long translations and constrained screens. Validate images/fonts/links, form submission guards and no layout traps above the keyboard. Visual similarity cannot trade away semantics or responsive behavior. Declare reference/viewport/environment/tolerance before claiming pixel-perfect comparison.

## Mobile and device integration

Cover minimum/current supported OS and representative older/current hardware, physical devices first when available, then reused simulators/emulators. Test permission allow/deny/permanent denial/settings return; cold/warm/background start; home/lock/kill/resume; native Back and payment/browser overlays; offline/install/update state; app links/universal links; camera/sensors and resource release. Test actual upgrade retention rather than reinstalling clean and claiming migration.

Optical scanning needs real codes, physical camera, material/lighting/distance/angle and measured decode/routing behavior. Store screenshot/release tasks follow existing Goldie and platform gates across required devices/locales with Release artifacts. Distinguish debug, simulator, physical, archive, uploaded, submitted, reviewed and public states.

## Backend, APIs and databases

Verify schemas and status/error semantics, auth/ownership/tenant isolation, input boundaries, idempotency, transactions, parallel requests, uniqueness, ordering, pagination and rate-limit behavior. Test query-count or execution plans only when performance risk warrants it. Match the relevant database engine for lock/concurrency/migration claims; an in-memory database cannot establish production lock behavior.

Include jobs, retries, duplicate/out-of-order events, poison/dead-letter behavior, scheduled timezone rules, stale cache and invalidation, partial provider failure and worker rollout compatibility. Reconcile persistent state and side effects, not just HTTP responses.

## Security, data and compliance

Test actual authorization bypass surfaces, cross-account/tenant access, unsafe uploads/URLs/redirects, injection or serialization boundaries, token lifecycle, rate limits and secret leakage relevant to the feature. Use synthetic/redacted fixtures. Confirm data collection, retention/deletion, permission purposes and third-party SDK behavior match real disclosures when in scope.

Dependency/scanner results require applicability and exploitability triage; scan success is not a complete security assessment. A justified finding needs concrete source/reproduction and impact. Do not prescribe live penetration tests or traffic generation without scope and authorization.

## Performance, reliability and observability

Measure realistic workload/data and user-critical path, with a comparable baseline, time window, error rate and percentile/resource metric. Test sustained resource use, startup/cold cache, degraded dependencies, bounded concurrency and recovery where relevant. Record environment variation; do not claim statistically meaningful improvement from a single noisy run.

Verify logs/metrics can connect request -> state change -> provider/job where relevant, without exposing secrets. Simulate a relevant failure and show the intended alert/runbook signal in an authorized environment. An installed dashboard or notification configuration alone does not prove operational detection.

## Test-suite and CI integrity

Record exact suite/case selection, expected nonzero scope, skipped/quarantined cases, failure and exit code. Verify CI actually runs intended checks on the final revision. Document flaky-test root cause and a bounded correction; repeated reruns until green do not establish reliability. Do not weaken assertions, remove requirements or alter fixtures to conceal a failure.

Use targeted checks during iteration and one appropriate final gate once stable. Rerun affected evidence after changes; expand testing only for new failures, changed scope or unresolved risk. Do not spend the owner's time on redundant passing runs or implementation-mirroring tests.

## Matrix row

Use `CASE-ID | requirement/criterion | setup/candidate | trigger or interruption | exact expected behavior | method/evidence level | platform/role/locale | owner | result | proof/gap`. Every required case gets a disposition. The plan specifies which combinations are mandatory, which are sampled and why.
