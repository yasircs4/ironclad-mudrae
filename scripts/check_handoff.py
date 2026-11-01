#!/usr/bin/env python3
"""Read-only structural checks for an owner-pinned Ironclad handback contract."""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

KINDS = {
    'test_log', 'build_log', 'screenshot', 'recording', 'source_reference',
    'provider_readback', 'device_readback', 'owner_exception', 'artifact_manifest',
}
STATUSES = {'PASS', 'FAIL', 'BLOCKED', 'NOT_RUN', 'OWNER_ACCEPTED_EXCEPTION'}
IDENTIFIER = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z')
SHA256 = re.compile(r'[a-fA-F0-9]{64}\Z')


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON object key')
        result[key] = value
    return result


def read_json(path, expected_sha256=None):
    with path.open('rb') as stream:
        content = stream.read(4 * 1024 * 1024 + 1)
    if len(content) > 4 * 1024 * 1024:
        raise ValueError('JSON input exceeds 4 MiB')
    if expected_sha256 is not None and hashlib.sha256(content).hexdigest() != expected_sha256.lower():
        raise ValueError('Acceptance contract does not match the owner-pinned SHA-256')
    value = json.loads(content.decode('utf-8'), object_pairs_hook=no_duplicate_keys)
    if not isinstance(value, dict):
        raise ValueError('JSON input must be an object')
    return value


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def identifier(value):
    return isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None


def strings(value):
    return isinstance(value, list) and all(nonempty(item) for item in value)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def indexed(items, label):
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError(label + ' must be an array of objects')
    result = {}
    for item in items:
        key = item.get('id')
        if not identifier(key) or key in result:
            raise ValueError(label + ' has an invalid or duplicate ID')
        result[key] = item
    return result


def local_file(root, raw):
    if not nonempty(raw):
        raise ValueError('Missing evidence/report path')
    path = Path(raw)
    path = path if path.is_absolute() else root / path
    path = path.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
        raise ValueError('Evidence/report must be a nonempty file inside the submission root')
    return path


def validate(contract, manifest, root):
    errors, holds, exceptions = [], [], []
    if not integer(contract.get('schema_version')) or not integer(manifest.get('schema_version')) or contract['schema_version'] != 1 or manifest['schema_version'] != 1:
        raise ValueError('Unsupported or missing schema_version')
    if not identifier(contract.get('work_order_id')):
        raise ValueError('Contract needs a work_order_id')
    if manifest.get('work_order_id') != contract['work_order_id']:
        errors.append('Manifest does not match the contracted work order')
    expected = indexed(contract.get('criteria'), 'Contract criteria')
    if not expected:
        raise ValueError('Contract must contain at least one criterion')
    for key, criterion in expected.items():
        kinds = criterion.get('required_evidence')
        if not identifier(criterion.get('gate')) or not strings(kinds) or not kinds:
            raise ValueError('Each contract criterion needs a gate and evidence types')
        if len(kinds) != len(set(kinds)) or not set(kinds).issubset(KINDS):
            raise ValueError('Invalid/duplicate contracted evidence type')
        if 'required_cases' in criterion and not strings(criterion['required_cases']):
            raise ValueError('required_cases must be an array of nonempty case IDs')
        if criterion.get('required_cases') and 'test_log' not in kinds:
            raise ValueError('Named automated cases require contracted test_log evidence')
        minimum = criterion.get('minimum_cases', 1)
        if not integer(minimum) or minimum < 1:
            raise ValueError('minimum_cases must be a positive integer')
        if 'allow_skipped' in criterion and not isinstance(criterion['allow_skipped'], bool):
            raise ValueError('allow_skipped must be boolean')
    reports = contract.get('required_reports')
    if not strings(reports) or not reports:
        raise ValueError('Contract needs a nonempty required_reports list')
    for report in reports:
        try:
            local_file(root, report)
        except (OSError, ValueError, RuntimeError):
            errors.append('Required report is missing, empty or outside root: ' + report)

    candidate = manifest.get('candidate')
    if not isinstance(candidate, dict) or not identifier(candidate.get('id')):
        raise ValueError('Manifest needs a candidate with an ID')
    if not nonempty(candidate.get('source_revision')) or not nonempty(candidate.get('environment')):
        raise ValueError('Candidate needs source_revision and target environment')
    if contract.get('required_environment') not in (None, candidate['environment']):
        errors.append('Candidate environment differs from contract')
    submitted = indexed(manifest.get('criteria'), 'Submitted criteria')
    evidence = indexed(manifest.get('evidence'), 'Evidence')
    missing, extra = set(expected) - set(submitted), set(submitted) - set(expected)
    errors.extend('Missing criterion: ' + key for key in sorted(missing))
    errors.extend('Uncontracted criterion: ' + key for key in sorted(extra))

    for key, item in evidence.items():
        if item.get('kind') not in KINDS:
            errors.append(key + ': unsupported evidence type')
        if item.get('candidate_id') != candidate['id'] or item.get('environment') != candidate['environment']:
            errors.append(key + ': candidate/environment mismatch')
        if not nonempty(item.get('description')):
            errors.append(key + ': missing observation description')
        try:
            stamp = datetime.fromisoformat(str(item.get('observed_at', '')).replace('Z', '+00:00'))
            if stamp.tzinfo is None:
                raise ValueError('Timezone missing')
        except ValueError:
            errors.append(key + ': invalid capture timestamp/timezone')
        try:
            path = local_file(root, item.get('path'))
            checksum = item.get('sha256')
            if not isinstance(checksum, str) or not SHA256.fullmatch(checksum) or digest(path) != checksum.lower():
                errors.append(key + ': evidence SHA-256 missing or mismatched')
            if item.get('kind') == 'screenshot':
                with path.open('rb') as stream:
                    header = stream.read(24)
                if not (header.startswith(b'\x89PNG\r\n\x1a\n') and header[12:16] == b'IHDR') and not header.startswith(b'\xff\xd8\xff'):
                    errors.append(key + ': screenshot is not a recognized PNG/JPEG header')
        except (OSError, ValueError, RuntimeError):
            errors.append(key + ': missing, empty or unsafe evidence file')

    for key in sorted(set(expected) & set(submitted)):
        row, requirement = submitted[key], expected[key]
        status = row.get('status')
        if status not in STATUSES:
            errors.append(key + ': invalid result status')
            continue
        references = row.get('evidence_ids')
        if not strings(references) or len(references) != len(set(references)):
            errors.append(key + ': evidence_ids must be unique strings')
            continue
        unknown = set(references) - set(evidence)
        if unknown:
            errors.append(key + ': unknown evidence reference')
        records = [evidence[ref] for ref in references if ref in evidence]
        if status in {'FAIL', 'BLOCKED', 'NOT_RUN'}:
            holds.append(key + ': ' + status)
            if not nonempty(row.get('reason')):
                errors.append(key + ': nonpassing status requires a reason')
            continue
        if status == 'OWNER_ACCEPTED_EXCEPTION':
            if not nonempty(row.get('reason')):
                errors.append(key + ': exception requires a reason and residual impact')
            authority = row.get('exception_evidence_id')
            if authority not in references or authority not in evidence or evidence[authority].get('kind') != 'owner_exception':
                errors.append(key + ': exception requires referenced owner-decision evidence')
            exceptions.append(key)
            continue
        present = {record.get('kind') for record in records}
        if not set(requirement['required_evidence']).issubset(present):
            errors.append(key + ': required evidence class is missing')
        cases = set()
        for record in records:
            if record.get('kind') in {'test_log', 'build_log'}:
                run = record.get('run')
                if not isinstance(run, dict) or not nonempty(run.get('command')) or not nonempty(run.get('cwd')) or not Path(run['cwd']).is_absolute():
                    errors.append(key + ': command evidence needs command and absolute cwd')
                    continue
                if not integer(run.get('exit_code')) or run['exit_code'] != 0:
                    errors.append(key + ': PASS references an unsuccessful/unknown command')
                if record['kind'] == 'test_log':
                    wanted, observed, skipped = (run.get(field) for field in ('expected_cases', 'observed_cases', 'skipped_cases'))
                    if not all(integer(value) for value in (wanted, observed, skipped)) or min(wanted, observed) < requirement.get('minimum_cases', 1) or wanted != observed or skipped < 0:
                        errors.append(key + ': empty, inconsistent or insufficient test coverage')
                    elif skipped and not requirement.get('allow_skipped', False):
                        errors.append(key + ': skipped tests are not allowed by contract')
                    case_ids = run.get('passed_case_ids', [])
                    if not strings(case_ids) or len(case_ids) != len(set(case_ids)):
                        errors.append(key + ': passed_case_ids must be unique strings')
                    elif integer(observed) and len(case_ids) > observed:
                        errors.append(key + ': named executed cases exceed observed test count')
                    else:
                        cases.update(case_ids)
        if not set(requirement.get('required_cases', [])).issubset(cases):
            errors.append(key + ': required executed case IDs are missing')

    gates = {}
    for row in expected.values():
        gates[row['gate']] = 'PENDING_SEMANTIC_REVIEW'
    return {
        'verdict': 'INCOMPLETE' if errors else ('HOLD' if holds else 'STRUCTURALLY_COMPLETE_PENDING_REVIEW'),
        'release_authorized': False,
        'semantic_review_required': True,
        'expected_criteria': len(expected),
        'submitted_status_counts': dict(Counter(row.get('status', 'MISSING') for row in submitted.values() if isinstance(row.get('status', ''), str))),
        'gates': gates,
        'owner_exceptions_requiring_review': exceptions,
        'errors': errors,
        'holds': holds,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--contract-sha256', required=True, help='Hash pinned by the owner in the work order')
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True, help='Submission root; evidence must stay inside it')
    args = parser.parse_args(argv)
    try:
        if not SHA256.fullmatch(args.contract_sha256):
            raise ValueError('Invalid owner-pinned SHA-256 format')
        contract = read_json(args.contract, expected_sha256=args.contract_sha256)
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Submission root must be a directory')
        manifest_path = local_file(root, str(args.manifest.resolve(strict=True)))
        result = validate(contract, read_json(manifest_path), root)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({'verdict': 'INVALID_INPUT', 'release_authorized': False, 'semantic_review_required': True, 'error': str(error)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['verdict'] == 'STRUCTURALLY_COMPLETE_PENDING_REVIEW' else 1


if __name__ == '__main__':
    sys.exit(main())
