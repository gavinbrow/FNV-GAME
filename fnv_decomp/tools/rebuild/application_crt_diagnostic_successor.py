"""Prepare a separate four-binding CRT diagnostic response from accepted V5.

Metadata only. This never invokes LINK, compiles code, or executes an image.
"""
import argparse
import json
from pathlib import Path

import application_link_diagnostic as diagnostic
import crt_adoption_consumer_contract as contract
import crt_provider_adoption_plan as planner

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'build/rebuild/application-link-diagnostic-v5/receipt.json': '480cf04bdd2370c41a88c047c0803803f085e864d2f5a26777a1e66c5d911fe8',
    'build/rebuild/application-link-diagnostic-v5/link.rsp': 'f145d5be8844b499744d21ec9a91f677242079990522714f13d438a14b730ac2',
    'build/rebuild/application-link-diagnostic-v5/link-receipt.json': '28a6b3aa2ba0cade82d6fcdab089f15ff1dbe5f3b91af72846a5886a0be5c380',
    'build/rebuild/application-link-diagnostic-v5/independent-outcome-review.json': '911ff85b6c4a2450f983cfcda1bce8505abaf3191707db7e06b7b2c4fc578292',
    'build/rebuild/application-cohort-observation-v1/receipt.json': '9848b08bfd51244412700d25cd9cc53136253e90117a4c3b67b03c347961586b',
    'build/rebuild/application-crt-adoption-plan-v1.json': contract.PLAN,
    'build/rebuild/application-crt-adoption-plan-peer-lane04-v1.json': contract.REVIEW,
    'build/rebuild/application-crt-adoption-v4-proposal-v1.rsp': contract.RESPONSE,
    'build/rebuild/crt-adoption-consumer-contract-peer-lane04-v1.json': 'a6c1d35a55a3e3e2c38d0dfcceb22cdfc5164a8a4d82da83f8561370a6854e8f',
    'tools/rebuild/crt_adoption_consumer_contract.py': 'cb724fdf907898f68577ef6a25774d4e38111562ea7e2020cc44c747d147448c',
    'tools/rebuild/crt_provider_adoption_plan.py': '7e17f4d0d951447967ccd9d98709e81e6ed4c93612de20d34a1ffdcaddfeb604',
    'tools/rebuild/application_link_diagnostic.py': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379',
}

def require(ok, message):
    if not ok: raise ValueError(message)

def successor_tokens(text, old_out, new_out, aliases):
    """Change exactly two output destinations and append four reviewed tokens."""
    lines = text.splitlines()
    require(all(line.startswith('"') and line.endswith('"') and len(line) > 2 for line in lines), 'malformed baseline response')
    tokens = [line[1:-1] for line in lines]
    before = list(tokens)
    for prefix, name in (('/OUT:', 'diagnostic.exe'), ('/MAP:', 'diagnostic.map')):
        old = prefix + str(old_out / name)
        require(tokens.count(old) == 1, 'one exact baseline output destination required')
        tokens[tokens.index(old)] = prefix + str(new_out / name)
    require(len(aliases) == 4 and len(set(aliases)) == 4 and all(a.startswith('/ALTERNATENAME:') for a in aliases), 'four unique alias tokens required')
    prior = [token.split('=', 1)[0] for token in before if token.startswith('/ALTERNATENAME:')]
    require(not set(prior).intersection(a.split('=', 1)[0] for a in aliases), 'canonical alias already present')
    tokens.extend(aliases)
    diagnostic.response_text(tokens)
    return tokens

def prepare(repository, out, expected_self, tests_sha256):
    repository, out = Path(repository).resolve(), Path(out).absolute()
    require(out.resolve() == out and out.parent == repository / 'build/rebuild' and not out.exists(), 'exclusive direct private output required')
    pins = dict(PINS)
    pins['tools/rebuild/application_crt_diagnostic_successor.py'] = expected_self
    pins['tests/rebuild/test_application_crt_diagnostic_successor.py'] = tests_sha256
    bindings = []
    for name, expected in pins.items():
        require(diagnostic.file_hash(repository / name) == expected, 'source/input pin differs: ' + name)
        bindings.append(diagnostic.identity(repository / name))
    old_out = repository / 'build/rebuild/application-link-diagnostic-v5'
    report = json.loads((old_out / 'receipt.json').read_text())
    diagnostic.stable(report['input_bindings'])
    require(report['status'] == 'prepared-no-native-LINK' and report['native_LINK_performed'] is False and report['whole_DATA_included'] is False, 'accepted prepared diagnostic required')
    require(report['selected_game_function_provider_count'] == 14329 and report['full_included_field_count'] == 44353 and len(report['aliases']) == 26 and all(a['enabled'] for a in report['aliases']), 'fixed V5 cohort required')
    fields = [row for group in report['provenance'].values() for row in group if row.get('proof')]
    observation = json.loads((repository / 'build/rebuild/application-cohort-observation-v1/receipt.json').read_text())
    # The accepted namespace contains every selected CODE/DATA definition plus
    # deferred EH candidates. This conservative superset can only reject more.
    strong = observation['provider_namespace']['symbols']
    gate = contract.validate((repository / 'build/rebuild/application-crt-adoption-plan-v1.json').read_bytes(),
        (repository / 'build/rebuild/application-crt-adoption-plan-peer-lane04-v1.json').read_bytes(),
        (repository / 'build/rebuild/application-crt-adoption-v4-proposal-v1.rsp').read_bytes(),
        'prospective_expanded_cohort', fields, strong)
    plan = json.loads((repository / 'build/rebuild/application-crt-adoption-plan-v1.json').read_text())
    require(diagnostic.file_hash(repository / 'build/units.json') == plan['units_sha256'], 'CRT recipe proof ancestry differs')
    bindings.append(diagnostic.identity(repository / 'build/units.json'))
    for name, expected in plan['inputs'].items():
        path = repository / 'build/rebuild' / name
        require(diagnostic.file_hash(path) == expected, 'CRT evidence ancestry differs: ' + name)
        bindings.append(diagnostic.identity(path))
    for name, expected in plan['sources'].items():
        path = repository / name
        require(diagnostic.file_hash(path) == expected, 'CRT source ancestry differs: ' + name)
        bindings.append(diagnostic.identity(path))
    for row in plan['prospective_expanded_cohort']['bindings']:
        require(row['normal_provider']['archive_sha256'] == report['default_libraries']['libcmt.lib']['sha256'], 'CRT provider archive differs from selected normal library')
    tokens = successor_tokens((old_out / 'link.rsp').read_text(), old_out, out, gate['tokens'])
    report.update(kind='separate-four-binding-CRT-link-diagnostic', status='prepared-no-native-LINK',
        command=[report['command'][0], '@' + str(out / 'link.rsp')],
        CRT_diagnostic_bindings=gate, CRT_input_namespace_is_conservative_superset=True,
        baseline_V5_actual_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v5/link-receipt.json'],
        runtime_ABI_approved=False, provider_adopted=False, runtime_eligible=False)
    report['input_bindings'].extend(bindings)
    diagnostic.stable(report['input_bindings'])
    out.mkdir()
    (out / 'link.rsp').write_text(diagnostic.response_text(tokens), encoding='utf-8')
    report['response_sha256'] = diagnostic.file_hash(out / 'link.rsp')
    with (out / 'receipt.json').open('x', encoding='utf-8') as stream: json.dump(report, stream, separators=(',', ':'))
    diagnostic.stable(report['input_bindings'])
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--tests-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = prepare(ROOT, args.out, args.source_sha256, args.tests_sha256)
    print(json.dumps(dict(status=result['status'], response_sha256=result['response_sha256'], CRT_bindings=4,
        CRT_field_uses=result['CRT_diagnostic_bindings']['alias_field_count'], native_LINK_performed=False)))

if __name__ == '__main__': main()
