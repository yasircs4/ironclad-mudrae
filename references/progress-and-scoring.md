# Completion, evidence and accepted progress

Use for multi-package work or whenever the owner requests a completion percentage. A percentage describes the defined assignment and evidence layer; it is not a forecast, quality probability or percentage of an entire product unless the contract explicitly covers that product.

## Fix the denominator in the work order

Before execution, list stable acceptance IDs with weights totaling 100, or use equal weights for a genuinely small uniform set. Weight business/correctness impact and effort sensibly; explain the basis. Keep critical gates mandatory regardless of weight. Separate new scope from already accepted work. The developer cannot lower weights, remove blocked criteria or renormalize the denominator.

| Number | Meaning | Authority |
|---|---|---|
| Developer-claimed implementation | Executor's claimed implemented scope, labeled unverified | Developer |
| Evidence packaging | Required artifacts structurally present for the stated scope | Checker/reviewer; presence is not acceptance |
| Manager-verified completion | Sum of fixed weights for criteria accepted PASS after semantic/source/runtime review | Reviewer acting under the owner's contract |

The handback checker does not compute weighted completion or authenticate human approval. Do not label its successful packaging result a 100% implementation or acceptance score.

## Award verified points

Verified percentage = accepted PASS weights / fixed total weight x 100. A criterion earns its full weight only when all of its agreed mandatory behavior and evidence are accepted. Partial, FAIL, BLOCKED, NOT_RUN and missing/unreviewed criteria earn zero verified points. Split genuinely separable milestones before execution if partial credit is needed; do not invent fractions after seeing the outcome.

OWNER_ACCEPTED_EXCEPTION has a separate waived-points total and the exact owner's authority, residual risk and affected gate. It never silently becomes verified PASS. Report accepted points, waived points and unresolved points so the totals remain explainable. Owner-authorized scope changes need a new version and an old-to-new crosswalk; show both the prior and revised basis.

Example: of 100 contracted points, 72 are accepted, eight waived, 12 blocked and eight failed. Report 72% verified completion, eight waived points, 20 unresolved points and the actual release verdict. Do not report 80% verified or divide by the 80 currently runnable points.

## Return an actionable review

Include scope/order version, candidate, review date, accepted criterion IDs/weights, unverified claims, blockers and rework. Explain the largest gaps and name their owner, required next evidence and bounded exit. Overall verdict follows acceptance-review.md; a high score cannot bypass a mandatory financial, privacy, hardware or release gate.

Before the first handback, verified acceptance is zero reviewed points for that order and implementation percentage is unknown. Say explicitly that this does not mean the existing application is 0% built. At 100% accepted, deployment or public submission still requires its own applicable authorization and readback.
