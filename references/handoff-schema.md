# Pinned acceptance contract and handback checker

Use for new critical, repeated or multi-package work orders where automatic completeness checks reduce omissions. Keep the human-readable order authoritative for semantics. Do not retrofit new mandatory artifacts onto previously issued work without an explicit order update.

## Ownership and invocation

The **manager** writes `acceptance-contract.json` beside the work order, computes SHA-256 and records that literal hash and the exact checker command in the order. The **developer** writes `handoff-manifest.json` inside the immutable submission root. The developer cannot weaken the contract or replace the pinned hash. Any contract change requires the owner's documented version change and revalidation of affected work.

Run the installed `scripts/check_handoff.py` using Python 3.9+ with:

| Argument | Value |
|---|---|
| `--contract` | Absolute manager-authored contract path |
| `--contract-sha256` | Literal owner-pinned 64-hex hash, not a newly computed hash of the developer's replacement |
| `--manifest` | Absolute developer manifest path inside the submission |
| `--root` | Absolute submission directory |

The checker reads local files only. It does not run commands from a report, access the network, change project files, evaluate code or grant release permission. Preserve its JSON output as mechanical validation evidence.

## Contract fields, version 1

```json
{
  "schema_version": 1,
  "work_order_id": "ORDER-01",
  "required_environment": "staging",
  "required_reports": ["REPORT.md", "REQUIREMENTS.md", "VALIDATION.md", "RISKS.md", "evidence/INDEX.md"],
  "criteria": [
    {
      "id": "AC-01",
      "gate": "functional",
      "required_evidence": ["test_log", "screenshot"],
      "minimum_cases": 2,
      "required_cases": ["CASE-01", "CASE-02"],
      "allow_skipped": false
    }
  ]
}
```

This is a schema example, not a universal test count or environment. Fill actual criteria, evidence classes, known case IDs and report paths from the plan. `required_environment`, `minimum_cases`, `required_cases` and `allow_skipped` are optional; defaults are no fixed environment, one executed case, no named case list and no skipped tests. A contract must have at least one criterion and one required report. IDs are unique, 1 to 80 alphanumeric/dot/underscore/hyphen characters starting alphanumeric.

`minimum_cases` applies to **each referenced test log**, while `required_cases` is the union of named successfully executed cases across those logs. If cases are distributed across focused runs, use a per-log minimum appropriate to those runs (often one), then require the exact case IDs. Do not set an aggregate suite total as the per-log minimum.

Manual review, screenshots, device observations and provider reconciliation are criteria with their own evidence kinds, not executed automated cases. For example, a real sandbox criterion can require `["provider_readback", "source_reference"]` and omit `required_cases`; a concurrent-callback criterion requires `test_log` with its automated case IDs. Named `required_cases` therefore requires contracted `test_log` evidence. Use separate criterion IDs when manual and automated acceptance need independent dispositions.

Allowed evidence kinds: `test_log`, `build_log`, `screenshot`, `recording`, `source_reference`, `provider_readback`, `device_readback`, `owner_exception`, `artifact_manifest`. Choose kinds for the claim; do not require a screenshot for an invisible storage invariant. Real/sandbox/physical identity remains in descriptions and reports for semantic inspection; the checker cannot authenticate a provider or device.

## Manifest fields, version 1

Root fields are `schema_version`, matching `work_order_id`, `candidate`, `criteria` and `evidence` arrays. Candidate contains a stable `id`, actual `source_revision` and target `environment`. Record dirty-diff identity, backend/build hashes and configuration provenance in the Markdown handback and artifact evidence.

Each criterion has the contracted `id`, `status` and unique `evidence_ids`. All required criteria must appear exactly once; uncontracted criteria cannot hide omissions. Status is PASS, FAIL, BLOCKED, NOT_RUN or OWNER_ACCEPTED_EXCEPTION. Nonpassing rows require a reason. An exception additionally needs `exception_evidence_id` referring to included `owner_exception` evidence. Its actual human authority must still be reviewed; a developer-authored note is not automatically an owner exception.

Each evidence item has `id`, `kind`, `path`, `sha256`, matching `candidate_id`, target `environment`, timezone-aware ISO `observed_at` and an observation `description`. Hash the delivered final redacted artifact and label redactions; preserve sensitive originals only in approved protected storage. Evidence/report files must be nonempty and resolve inside the submission root, including through symlinks. Keep earlier candidate/failure artifacts in the history/index; final manifest evidence must identify the final candidate.

Command evidence (`test_log`/`build_log`) referenced by PASS requires `run.command`, absolute `run.cwd` and integer `run.exit_code` equal to zero. A test log also needs integer `expected_cases`, `observed_cases`, `skipped_cases`, plus `passed_case_ids` when named cases are contracted. Expected and observed execution counts must agree and meet the manager's minimum. Only successfully executed case IDs belong in `passed_case_ids`. Reporting fields are claims to verify against actual logs, not proof of truth by themselves.

Named executed case IDs must be unique and cannot exceed the observed count. They may be a subset of a larger suite. An owner exception needs both a reason/residual impact and referenced owner-decision evidence; its authority is still reviewed manually. The pinned contract hash is checked against the exact JSON bytes parsed.

PNG/JPEG header checks catch mislabeled text files, not a loading screen, a fabricated image, malformed image internals or semantic correctness. Recordings and provider files are checked for presence/hash, not content validity. Inspect them during review.

## Results and limits

| Exit | Verdict | Meaning |
|---|---|---|
| 0 | STRUCTURALLY_COMPLETE_PENDING_REVIEW | Required packaging/identity/hash checks passed; semantic review still mandatory |
| 1 | INCOMPLETE or HOLD | Missing/mismatched proof or criteria, failed requirements, blocked/not-run work |
| 2 | INVALID_INPUT | Invalid schema/JSON/paths or contract hash mismatch |

Every output has `release_authorized: false` and `semantic_review_required: true`. A structural pass is never ACCEPTED, production-ready, provider-verified or release authorization. An agent can write false claims into a manifest; source, log, screenshot and provider inspection remain necessary. Independently pinning the contract prevents accidental acceptance weakening, not all deliberate tampering.

## Skill-maintenance validation

From the installed skill directory, run `python3 -m unittest discover -s scripts -p 'test_*.py' -v` after changing the checker. Tests use isolated temporary fixtures, not application code, live services or actual private data. Also run your available Agent Skills validator after changing the entry point or metadata.
