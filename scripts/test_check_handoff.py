"""Behavioral checks for the read-only handback validator, using temporary fixtures."""

from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import check_handoff as checker


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'submission'
        self.root.mkdir()
        for name in ['REPORT.md', 'REQUIREMENTS.md', 'VALIDATION.md', 'RISKS.md', 'evidence/INDEX.md']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Fixture report, not a reviewed outcome.\n')
        (self.root / 'evidence/run.log').write_text('CASE-01 PASS\nCASE-02 PASS\n')
        # The checker intentionally checks headers only, never semantic image validity.
        (self.root / 'evidence/screen.png').write_bytes(b'\x89PNG\r\n\x1a\n' + b'\0\0\0\rIHDR' + b'\0' * 16)
        self.contract = {
            'schema_version': 1, 'work_order_id': 'ORDER-01', 'required_environment': 'staging',
            'required_reports': ['REPORT.md', 'REQUIREMENTS.md', 'VALIDATION.md', 'RISKS.md', 'evidence/INDEX.md'],
            'criteria': [{'id': 'AC-01', 'gate': 'functional', 'required_evidence': ['test_log', 'screenshot'], 'minimum_cases': 2, 'required_cases': ['CASE-01', 'CASE-02']}],
        }
        self.manifest = {
            'schema_version': 1, 'work_order_id': 'ORDER-01',
            'candidate': {'id': 'candidate-1', 'source_revision': 'fixture-revision', 'environment': 'staging'},
            'criteria': [{'id': 'AC-01', 'status': 'PASS', 'evidence_ids': ['TEST-01', 'IMAGE-01']}],
            'evidence': [self.evidence('TEST-01', 'test_log', 'evidence/run.log'), self.evidence('IMAGE-01', 'screenshot', 'evidence/screen.png')],
        }
        self.manifest['evidence'][0]['run'] = {
            'command': 'fixture-test-command', 'cwd': str(self.root), 'exit_code': 0,
            'expected_cases': 2, 'observed_cases': 2, 'skipped_cases': 0,
            'passed_case_ids': ['CASE-01', 'CASE-02'],
        }

    def evidence(self, key, kind, path):
        return {
            'id': key, 'kind': kind, 'path': path, 'sha256': checker.digest(self.root / path),
            'candidate_id': 'candidate-1', 'environment': 'staging',
            'observed_at': '2026-11-01T12:00:00+03:00', 'description': 'Controlled test fixture only',
        }

    def run_check(self):
        return checker.validate(self.contract, self.manifest, self.root)

    def assert_incomplete(self):
        result = self.run_check()
        self.assertEqual(result['verdict'], 'INCOMPLETE')
        self.assertTrue(result['errors'])
        self.assertFalse(result['release_authorized'])

    def cli(self, pinned=None):
        contract_path = self.base / 'contract.json'
        contract_path.write_text(json.dumps(self.contract))
        manifest_path = self.root / 'handoff-manifest.json'
        manifest_path.write_text(json.dumps(self.manifest))
        output = io.StringIO()
        with redirect_stdout(output):
            code = checker.main(['--contract', str(contract_path), '--contract-sha256', pinned or checker.digest(contract_path), '--manifest', str(manifest_path), '--root', str(self.root)])
        return code, json.loads(output.getvalue())

    def test_complete_structure_never_grants_acceptance_or_release(self):
        code, result = self.cli()
        self.assertEqual(code, 0)
        self.assertEqual(result['verdict'], 'STRUCTURALLY_COMPLETE_PENDING_REVIEW')
        self.assertFalse(result['release_authorized'])
        self.assertTrue(result['semantic_review_required'])

    def test_missing_criterion_is_detected(self):
        self.manifest['criteria'] = []
        self.assert_incomplete()

    def test_extra_criterion_is_detected(self):
        self.manifest['criteria'].append({'id': 'AC-02', 'status': 'PASS', 'evidence_ids': []})
        self.assert_incomplete()

    def test_empty_contract_is_invalid(self):
        self.contract['criteria'] = []
        with self.assertRaises(ValueError):
            self.run_check()

    def test_manual_criterion_cannot_require_automated_case_ids(self):
        self.contract['criteria'][0]['required_evidence'] = ['provider_readback']
        with self.assertRaises(ValueError):
            self.run_check()

    def test_duplicate_criterion_is_invalid(self):
        self.manifest['criteria'].append(copy.deepcopy(self.manifest['criteria'][0]))
        with self.assertRaises(ValueError):
            self.run_check()

    def test_pinned_contract_cannot_be_replaced(self):
        code, result = self.cli('0' * 64)
        self.assertEqual(code, 2)
        self.assertEqual(result['verdict'], 'INVALID_INPUT')

    def test_evidence_tamper_is_detected(self):
        (self.root / 'evidence/run.log').write_text('Different content')
        self.assert_incomplete()

    def test_missing_required_evidence_class_is_detected(self):
        self.manifest['criteria'][0]['evidence_ids'] = ['TEST-01']
        self.assert_incomplete()

    def test_failed_command_cannot_support_pass(self):
        self.manifest['evidence'][0]['run']['exit_code'] = 1
        self.assert_incomplete()

    def test_empty_test_run_cannot_support_pass(self):
        self.manifest['evidence'][0]['run'].update(expected_cases=0, observed_cases=0)
        self.assert_incomplete()

    def test_missing_named_case_is_detected_even_with_sufficient_count(self):
        self.manifest['evidence'][0]['run']['passed_case_ids'] = ['CASE-01', 'CASE-99']
        self.assert_incomplete()

    def test_named_cases_cannot_exceed_observed_count(self):
        self.contract['criteria'][0]['minimum_cases'] = 1
        self.manifest['evidence'][0]['run'].update(expected_cases=1, observed_cases=1)
        self.assert_incomplete()

    def test_duplicate_named_cases_are_rejected(self):
        self.manifest['evidence'][0]['run']['passed_case_ids'] = ['CASE-01', 'CASE-01']
        self.assert_incomplete()

    def test_skips_require_owner_contract_permission(self):
        self.manifest['evidence'][0]['run']['skipped_cases'] = 1
        self.assert_incomplete()
        self.contract['criteria'][0]['allow_skipped'] = True
        self.assertEqual(self.run_check()['verdict'], 'STRUCTURALLY_COMPLETE_PENDING_REVIEW')

    def test_candidate_mismatch_is_detected(self):
        self.manifest['evidence'][0]['candidate_id'] = 'old-candidate'
        self.assert_incomplete()

    def test_environment_mismatch_is_detected(self):
        self.manifest['candidate']['environment'] = 'production'
        self.assert_incomplete()

    def test_text_file_renamed_png_is_not_image_evidence(self):
        path = self.root / 'evidence/screen.png'
        path.write_text('Not an image')
        self.manifest['evidence'][1]['sha256'] = checker.digest(path)
        self.assert_incomplete()

    def test_path_traversal_is_rejected(self):
        outside = self.base / 'outside.log'
        outside.write_text('Outside evidence')
        self.manifest['evidence'][0].update(path='../outside.log', sha256=checker.digest(outside))
        self.assert_incomplete()

    def test_symlink_escape_is_rejected(self):
        outside = self.base / 'outside.log'
        outside.write_text('Outside evidence')
        (self.root / 'evidence/escape.log').symlink_to(outside)
        self.manifest['evidence'][0].update(path='evidence/escape.log', sha256=checker.digest(outside))
        self.assert_incomplete()

    def test_missing_report_is_detected(self):
        (self.root / 'RISKS.md').unlink()
        self.assert_incomplete()

    def test_blocker_remains_hold(self):
        self.manifest['criteria'][0].update(status='BLOCKED', reason='Physical device unavailable')
        code, result = self.cli()
        self.assertEqual(code, 1)
        self.assertEqual(result['verdict'], 'HOLD')

    def test_exception_without_owner_evidence_is_incomplete(self):
        self.manifest['criteria'][0].update(status='OWNER_ACCEPTED_EXCEPTION', exception_evidence_id='MISSING')
        self.assert_incomplete()

    def test_exception_evidence_still_requires_human_review(self):
        path = self.root / 'evidence/owner.md'
        path.write_text('Synthetic owner-decision fixture; authority not authenticated.')
        self.manifest['evidence'].append(self.evidence('OWNER-01', 'owner_exception', 'evidence/owner.md'))
        self.manifest['criteria'][0].update(status='OWNER_ACCEPTED_EXCEPTION', reason='Fixture-only exception; actual authority remains for review', exception_evidence_id='OWNER-01', evidence_ids=['OWNER-01'])
        result = self.run_check()
        self.assertEqual(result['owner_exceptions_requiring_review'], ['AC-01'])
        self.assertTrue(result['semantic_review_required'])
        self.assertFalse(result['release_authorized'])

    def test_exception_cannot_omit_reason(self):
        path = self.root / 'evidence/owner.md'
        path.write_text('Synthetic owner decision')
        self.manifest['evidence'].append(self.evidence('OWNER-01', 'owner_exception', 'evidence/owner.md'))
        self.manifest['criteria'][0].update(status='OWNER_ACCEPTED_EXCEPTION', exception_evidence_id='OWNER-01', evidence_ids=['OWNER-01'])
        self.assert_incomplete()

    def test_boolean_schema_version_is_not_integer_version(self):
        self.contract['schema_version'] = True
        with self.assertRaises(ValueError):
            self.run_check()

    def test_hash_is_checked_on_exact_parsed_contract_bytes(self):
        path = self.base / 'contract.json'
        path.write_text(json.dumps(self.contract))
        pinned = checker.digest(path)
        path.write_text(json.dumps({**self.contract, 'criteria': []}))
        with self.assertRaises(ValueError):
            checker.read_json(path, expected_sha256=pinned)

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        path = self.base / 'duplicate.json'
        path.write_text('{"schema_version":1,"schema_version":2}')
        with self.assertRaises(ValueError):
            checker.read_json(path)

    def test_check_does_not_mutate_submission_files(self):
        before = {str(path.relative_to(self.root)): checker.digest(path) for path in self.root.rglob('*') if path.is_file()}
        self.run_check()
        after = {str(path.relative_to(self.root)): checker.digest(path) for path in self.root.rglob('*') if path.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
