# Ironclad-mudrae

**A manager-first Agent Skill for developer work orders and evidence-based acceptance.**

Turn a feature headline into technical decisions, bounded developer assignments, QA cases and a reviewable handback. Keep planning, implementation, verification and release as separate responsibilities.

Authored by [Yasir Najeep](https://yasirnajeep.com/). Released under [MIT](LICENSE). Skill version: **2.1.0**. The portable identifier is `ironclad-mudrae`; the display name is **Ironclad-mudrae**. The owner has reserved the Arabic rendering for a later update.

## What it does

- **PLAN:** establish facts, make critical architecture/recovery decisions, sequence packages and fix acceptance before dispatch. This is the default.
- **REVIEW:** inspect developer reports, source/diffs and actual proof; return ACCEPTED, CHANGES_REQUIRED or BLOCKED with bounded rework.
- **EXECUTOR:** guide an implementing agent only after the human explicitly assigns implementation of a work order.
- **Evidence contract:** issue a pinned acceptance contract and check handback structure, artifact hashes, candidate identity, required evidence kinds and named automated case claims.
- **Progress:** separate developer claims, evidence packaging and reviewer-accepted completion against a fixed denominator.

The reference playbooks cover requirements, architecture, durable state, concurrency, security/privacy, migrations, functional and visual QA, performance, provider/device proof, release, operations and incident recovery. Load only the references relevant to the assignment. Small reversible changes should stay small.

## Install

Once this repository is public, install with the [Skills CLI](https://skills.sh/docs):

```bash
pnpm dlx skills add yasircs4/ironclad-mudrae --skill ironclad-mudrae -g
```

Or place this complete directory, including `references/`, `scripts/` and `agents/`, in your host's supported skills directory. Follow that host's discovery rules and start a fresh session when required. The instructions use the open [Agent Skills format](https://agentskills.io/specification); actual loading and implicit invocation depend on the host. Codex UI metadata is included in `agents/openai.yaml`. There are no mandatory hosted-service, account or agent-framework dependencies. The optional local checker uses Python 3.9+ and only the standard library.

## Use it

### Plan a development assignment

```text
Use $ironclad-mudrae in PLAN mode.
Review this project's source and documentation without implementing it.
Make the technical decisions for durable offline caching and cart recovery.
Give the developer a work order with packages, failure cases, proof requirements
and a fixed acceptance scorecard. Keep actual deployment separately authorized.
```

Supply the actual repository, authoritative specification and constraints. If these are missing, the skill should issue a precise discovery package, not invent paths, APIs or test commands.

### Review the developer's report

```text
Use $ironclad-mudrae in REVIEW mode.
Inspect the original work order and the developer's REPORT.md, source diff
and referenced evidence. Tell me what is accepted, what is wrong, which gates
are blocked and the verified completion percentage. Issue bounded rework.
```

### Assign an executor

```text
You are assigned implementation of the attached work order.
Use $ironclad-mudrae in EXECUTOR mode and read references/executor-contract.md.
Implement the authorized scope, preserve failures and return the required
Markdown handback and actual evidence. Follow the order's action boundaries.
```

## The handback checker

The manager writes `acceptance-contract.json`, pins its literal SHA-256 in the work order and supplies the exact command. The developer returns `handoff-manifest.json` and the required reports/evidence. [The schema](references/handoff-schema.md) defines every field and evidence kind. [A synthetic example](examples/README.md) demonstrates the distinction between structural completion and acceptance.

Run from this repository to inspect the bundled example:

```bash
python3 scripts/check_handoff.py \
  --contract examples/acceptance-contract.json \
  --contract-sha256 9ad93e1ebf32a06c629f5c00c7dd1d0d7d849181e0731e39ada0fab129ef0c43 \
  --manifest examples/submission/handoff-manifest.json \
  --root examples/submission
```

The literal hash above belongs only to the bundled example. Real work orders must pin their own contract and exact paths; do not reuse the demo's requirements or hash.

| Exit | Result | What it means |
|---|---|---|
| 0 | STRUCTURALLY_COMPLETE_PENDING_REVIEW | Packaging checks passed; semantic review is still required |
| 1 | INCOMPLETE or HOLD | Missing/mismatched evidence or nonpassing criteria |
| 2 | INVALID_INPUT | Invalid schema, unsafe input path or contract-hash mismatch |

Every result sets `release_authorized: false`. The checker does not execute commands from reports, contact providers, compute weighted acceptance or establish whether logs/screenshots are truthful. Its PNG/JPEG check verifies a recognizable header, not image meaning or complete image validity. Never publish the synthetic example as application QA evidence.

## Verify and contribute

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

The tests use temporary synthetic fixtures. They exercise checker failure modes; they do not benchmark agent capability. For workflow changes, use the [behavioral exercises](references/behavioral-checks.md) and record the actual model/runtime, raw request, permitted resources, outputs and limitations. Independent evaluation adds confidence when available and authorized. No comparative model benchmark is claimed by this release.

Contributions should explain the observed failure, keep the correction proportional, add a meaningful regression where appropriate and preserve existing contracts. Keep credentials, private project data, real customer artifacts and machine-specific paths out of submissions.

## Related published approaches

Comparable work exists. [Superpowers](https://github.com/obra/superpowers) provides a development skill collection with planning, execution and verification. [Planning with Files](https://github.com/othmanadi/planning-with-files) focuses on persistent planning and context continuity. [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) provides plan/work/review/compound workflows. [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) is a broader role-based development framework. [BMAD-Speckit-SDD-Flow](https://github.com/milome/BMAD-Speckit-SDD-Flow) also documents requirement contracts, evidence chains and human closeout gates.

Ironclad-mudrae packages a specific manager-first workflow and a local handback completeness checker. It does not claim to invent planning, evidence gates or human review, to replace those projects, or to outperform them. Related-project descriptions are based on their primary documentation reviewed on 2026-11-02; integrations and interfaces may change.

## Limits

A skill is guidance, not a sandbox or an approval enforcement engine. It cannot grant missing tools, access or model competence, prevent all fabricated claims, certify software, guarantee store approval or authorize a public release. Source/runtime review and the appropriate provider/device evidence remain necessary. Existing project policies and human authority govern real actions.
