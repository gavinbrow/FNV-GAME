#!/usr/bin/env python3
"""Check saved build/harness evidence, without opening executable files.

This validates recorded evidence only; it neither reruns a build nor establishes
that a particular negative-control mutation was applied. Strict configuration
checks compare recorded identifiers, not the underlying build inputs.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def check(positive, default, controls, verdict):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def sha(run, label):
        value = run.get('exe', {}).get('sha256')
        require(isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{64}', value) is not None,
                label + ': invalid or absent saved SHA-256')
        return value.lower() if isinstance(value, str) else None
    def valid_build(run, label):
        require(run.get('status') in ('ok', 'ok-harness-skipped'), label + ': unsuccessful status')
        steps = run.get('steps')
        require(isinstance(steps, list) and bool(steps), label + ': missing build steps')
        if isinstance(steps, list):
            require(all(isinstance(s, dict) and s.get('rc') == 0 for s in steps), label + ': failed or malformed step')
    for label, run in [('positive', positive), ('default', default)] + [('control %d' % (i + 1), c) for i, c in enumerate(controls)]:
        valid_build(run, label)
    psha, dsha = sha(positive, 'positive'), sha(default, 'default')
    require(psha is not None and psha == dsha, 'positive and default saved hashes differ')
    require(positive.get('provenance', {}).get('m3', {}).get('negctl') is False,
            'positive is not explicitly marked non-control')
    require(not any(k in default.get('provenance', {}) for k in ('m3', 'm3_dv1', 'm3_error')),
            'default summary includes M3 provenance or error')
    require(not any(s.get('name') in ('m3-gen', 'm3-dv1') for s in default.get('steps', []) if isinstance(s, dict)),
            'default summary includes M3 build steps')
    require(len(controls) >= 2, 'at least two control summaries are required')
    control_hashes = []
    for i, control in enumerate(controls):
        label = 'control %d' % (i + 1)
        csha = sha(control, label)
        control_hashes.append(csha)
        require(csha is not None and psha is not None and csha != psha, label + ': hash does not differ from positive')
        require(control.get('provenance', {}).get('m3', {}).get('negctl') is True,
                label + ': not explicitly marked as negative control')
    require(len(set(control_hashes)) == len(control_hashes), 'control hashes are not distinct')
    harness = positive.get('harness')
    require(isinstance(harness, dict) and harness.get('rc') == 0 and harness.get('pass_') is True,
            'positive summary lacks passing harness')
    if not isinstance(harness, dict):
        harness = {}
    require(verdict.get('pass_') is True, 'saved harness verdict did not pass')
    require(verdict.get('exe') == positive.get('exe', {}).get('path'), 'verdict executable path does not match positive summary')
    steps = verdict.get('steps', {})
    require(steps == harness.get('steps'), 'harness steps disagree between summary and verdict')
    for key in ('main_menu_reached', 'world_loaded', 'alive_after_play', 'extended_ok', 'exited_cleanly'):
        require(steps.get(key) is True, 'harness missing ' + key)
    require(steps.get('exit_code') == 0, 'harness did not record exit code 0')
    require(isinstance(steps.get('play_secs'), (int, float)) and not isinstance(steps.get('play_secs'), bool) and steps['play_secs'] > 0,
            'harness missing positive gameplay duration')
    extended = steps.get('extended', {})
    for key in ('new_save_written', 'world_after_coc', 'world_after_time', 'world_after_load'):
        require(extended.get(key) is True, 'extended harness missing ' + key)
    return errors


def check_cell_state(verdict):
    """Require recorded cell transition, restoration, and actual input bindings."""
    steps = verdict.get('steps', {})
    ext = steps.get('extended', {})
    bindings = steps.get('quick_bindings', {})
    keys = ('cell_before_save', 'cell_after_save', 'cell_after_coc', 'cell_before_load', 'cell_after_load')
    valid = lambda x: type(x) is int and 0 < x <= 0xffffffff
    errors = []
    if not isinstance(ext, dict) or any(not valid(ext.get(k)) for k in keys):
        errors.append('missing or invalid cell IDs')
    elif not (ext['cell_before_save'] == ext['cell_after_save'] == ext['cell_after_load'] and
              ext['cell_after_coc'] == ext['cell_before_load'] != ext['cell_before_save']):
        errors.append('cell transition or restoration mismatch')
    if not isinstance(ext, dict) or ext.get('cell_changed') is not True or ext.get('cell_restored') is not True:
        errors.append('cell change/restoration flags missing')
    if not isinstance(bindings, dict) or any(not valid(bindings.get(k)) or bindings[k] > 255 for k in ('quicksave_scan', 'quickload_scan')):
        errors.append('missing or invalid quicksave/load scan codes')
    return errors


def check_extended_mode(run, label):
    """Check recorded stages and extended DV1 provenance; exact selection is not recorded."""
    names = {s.get('name') for s in run.get('steps', []) if isinstance(s, dict)}
    provenance = run.get('provenance', {})
    errors = []
    if not {'m3-gen', 'm3-dv1'}.issubset(names):
        errors.append(label + ': missing recorded M3/DV1 stages')
    if provenance.get('m3_dv1', {}).get('ext', {}).get('enabled') is not True:
        errors.append(label + ': extended DV1 provenance not enabled')
    if 'm3_error' in provenance:
        errors.append(label + ': M3 provenance error')
    return errors


def check_provenance(positive, others):
    """Check recorded code coverage and field-count consistency, not binary identity."""
    errors = []
    expected = {'code_coverage_pct_of_nonpadding_text': 100.0,
                'borrowed_relocation_field_bytes': 0, 'undecompiled_bytes': 0,
                'code_bytes_taken_from_filled_image': 0, 'filled_equals_reference': True}
    base = positive.get('provenance', {})
    counters = ('rel32_fields', 'dir32_fields', 'data_pointer_fields')
    for key, value in expected.items():
        if base.get(key) != value:
            errors.append('positive: unexpected provenance ' + key)
    for key in counters:
        value = base.get(key)
        if key == 'data_pointer_fields':
            valid = isinstance(value, dict) and bool(value) and all(type(v) is int and v >= 0 for v in value.values())
        else:
            valid = type(value) is int and value >= 0
        if not valid:
            errors.append('positive: missing or invalid provenance ' + key)
    for label, run in others:
        prov = run.get('provenance', {})
        for key in (*expected, *counters):
            if key not in prov or prov[key] != base.get(key):
                errors.append(label + ': provenance differs for ' + key)
    return errors


def check_recorded_config(positive, default, controls, selection, control_ids):
    """Compare recorded effective configuration with caller-supplied identifiers."""
    errors = []
    if not isinstance(selection, str) or not selection.strip():
        errors.append('expected selection must be a nonempty identifier')
    if len(control_ids) != len(controls):
        errors.append('expected control identifier count must match control summaries')
    if any(not isinstance(value, str) or not value.strip() for value in control_ids):
        errors.append('expected control identifiers must be nonempty')
    if 'unknown' in control_ids:
        errors.append('unknown is not an exact control identifier')
    if len(set(control_ids)) != len(control_ids):
        errors.append('expected control identifiers must be distinct')
    if 'm3_config' in default.get('provenance', {}):
        errors.append('default: unexpected M3 configuration')
    for label, run, expected_control in ([('positive', positive, None)] +
            [('control %d' % (i + 1), run, control_ids[i] if i < len(control_ids) else None)
             for i, run in enumerate(controls)]):
        config = run.get('provenance', {}).get('m3_config')
        if not isinstance(config, dict):
            errors.append(label + ': missing recorded M3 configuration')
            continue
        for key, expected in (('selection', selection), ('dv1', True),
                              ('dv1_ext', True), ('negative_control', expected_control)):
            if key not in config or (type(config[key]) is not type(expected) or config[key] != expected):
                errors.append(label + ': recorded M3 configuration differs for ' + key)
    return errors


def check_selection_sha256(positive, controls, expected):
    """Compare the recorded selection digest; do not read the selection file."""
    errors = []
    if not isinstance(expected, str) or re.fullmatch(r'[0-9a-fA-F]{64}', expected) is None:
        return ['expected selection SHA-256 must contain exactly 64 hexadecimal characters']
    for label, run in ([('positive', positive)] +
                       [('control %d' % (i + 1), run) for i, run in enumerate(controls)]):
        config = run.get('provenance', {}).get('m3_config')
        if not isinstance(config, dict):
            errors.append(label + ': missing recorded M3 configuration for selection SHA-256')
            continue
        recorded = config.get('selection_sha256')
        if not isinstance(recorded, str) or re.fullmatch(r'[0-9a-fA-F]{64}', recorded) is None:
            errors.append(label + ': missing or invalid recorded selection SHA-256')
        elif recorded.lower() != expected.lower():
            errors.append(label + ': recorded selection SHA-256 does not match expected digest')
    return errors


def check_control_logs(summary_path, summary):
    """Corroborate Batch 7 or 8 mutation label and expected diagnostic from saved logs."""
    names = {s.get('name'): s.get('log') for s in summary.get('steps', [])}
    root = summary_path.parent.resolve()
    def read_step(name):
        if not names.get(name):
            raise ValueError('missing %s log in summary' % name)
        path = (root / names[name]).resolve()
        if not path.is_relative_to(root):
            raise ValueError('log path escapes summary directory')
        return path.read_text(encoding='utf-8', errors='replace')
    gen, verify = read_step('m3-gen'), read_step('data-v3')
    gen_labels = re.findall(r'NEGATIVE CONTROL', gen)
    gen_matches = re.findall(r'NEGATIVE CONTROL \((b[78] (?:value|pointer)|p2 scalar value|p2 array value|p2 tail pointer|p2 BSAudio tail pointer|p2 bulk tail pointer)\):', gen)
    library_lines = re.findall(r'^.*NEGATIVE CONTROL \(p2 (?:library value|PSA value|PSA pointer|typeid value|typeid pointer|native literal value|native literal pointer|BSAudio value|BSAudio pointer|bulk value|bulk pointer)\):.*$', verify, re.M)
    if library_lines:
        if gen_labels or len(set(library_lines)) != 1:
            raise ValueError('ambiguous library mutation label')
        label = re.search(r'NEGATIVE CONTROL \(([^)]+)\):', library_lines[0]).group(1)
    else:
        if len(gen_labels) != 1 or len(gen_matches) != 1:
            raise ValueError('expected one supported mutation label')
        label = gen_matches[0]
    kind = 'pointer' if label.endswith('pointer') else 'value'
    ids = {'p2 scalar value':'p2sv', 'p2 array value':'p2av', 'p2 tail pointer':'p2wp', 'p2 library value':'p2lv', 'p2 PSA value':'p2rv', 'p2 PSA pointer':'p2rp', 'p2 typeid value':'p2tv', 'p2 typeid pointer':'p2tp', 'p2 native literal value':'p2nv', 'p2 native literal pointer':'p2np', 'p2 BSAudio value':'p2bv', 'p2 BSAudio pointer':'p2bp', 'p2 BSAudio tail pointer':'p2bw', 'p2 bulk value':'p2cv', 'p2 bulk pointer':'p2cp', 'p2 bulk tail pointer':'p2cw'}
    expected_id = ids.get(label) or label[:2] + ('p' if kind == 'pointer' else 'v')
    recorded = summary.get('provenance', {}).get('m3_config', {}).get('negative_control')
    if label in ('p2 PSA value', 'p2 PSA pointer'):
        expected_line = ('NEGATIVE CONTROL (p2 PSA value): VA 01196e20 offset 8 changed from 2e to 2f' if label.endswith('value') else
                         'NEGATIVE CONTROL (p2 PSA pointer): VA 0110fbe8 offset 12 changed from 01196e20 to 011831e8')
        if library_lines[0].strip() != expected_line:
            raise ValueError('PSA mutation detail mismatch')
        if recorded != expected_id:
            raise ValueError('missing or wrong PSA control identifier')
    if label in ('p2 typeid value', 'p2 typeid pointer'):
        expected_line = ('NEGATIVE CONTROL (p2 typeid value): VA 011b8140 offset 8 changed from 2e to 2f' if kind == 'value' else
                         'NEGATIVE CONTROL (p2 typeid pointer): VA 011b8140 offset 0 changed from 010f1ee0 to 010f1ee4')
        if library_lines[0].strip() != expected_line or recorded != expected_id:
            raise ValueError('typeid mutation detail or identifier mismatch')
    if label in ('p2 native literal value', 'p2 native literal pointer'):
        expected_line = ('NEGATIVE CONTROL (p2 native literal value): VA 01185d30 offset 8 changed from 2e to 2f' if kind == 'value' else
                         'NEGATIVE CONTROL (p2 native literal pointer): VA 01185d30 offset 0 changed from 010f1ee0 to 010f1ee4')
        if library_lines[0].strip() != expected_line or recorded != expected_id:
            raise ValueError('native literal mutation detail or identifier mismatch')
    if label in ('p2 BSAudio value', 'p2 BSAudio pointer'):
        expected_line = ('NEGATIVE CONTROL (p2 BSAudio value): VA 011ac95c offset 8 changed from 2e to 2f' if kind == 'value' else 'NEGATIVE CONTROL (p2 BSAudio pointer): VA 011ac95c offset 0 changed from 010f1ee0 to 010f1ee4')
        if library_lines[0].strip() != expected_line or recorded != expected_id: raise ValueError('BSAudio descriptor control detail or identifier mismatch')
    if label == 'p2 BSAudio tail pointer':
        line = 'NEGATIVE CONTROL (p2 BSAudio tail pointer): VA 011ac972 offset 2 changed from 010f1ee0 to 010f1ee4'
        if line not in gen.splitlines() or recorded != expected_id: raise ValueError('BSAudio tail control detail or identifier mismatch')
    if label in ('p2 bulk value', 'p2 bulk pointer'):
        expected_line = ('NEGATIVE CONTROL (p2 bulk value): VA 01183f7c offset 8 changed from 2e to 2f' if kind == 'value' else 'NEGATIVE CONTROL (p2 bulk pointer): VA 01183f7c offset 0 changed from 010f1ee0 to 010f1ee4')
        if library_lines[0].strip() != expected_line or recorded != expected_id: raise ValueError('bulk descriptor control detail or identifier mismatch')
    if label == 'p2 bulk tail pointer':
        line = 'NEGATIVE CONTROL (p2 bulk tail pointer): VA 01183f98 offset 0 changed from 010f1ee0 to 010f1ee4'
        if line not in gen.splitlines() or recorded != expected_id: raise ValueError('bulk tail control detail or identifier mismatch')
    if recorded is not None and recorded != expected_id:
        raise ValueError('mutation label disagrees with recorded control identifier')
    if 'ROUND TRIP FAILED' not in verify or 'negative control: failure is expected' not in verify:
        raise ValueError('missing expected round-trip failure evidence')
    diagnostic = 'M3 RELOC VALUE MISMATCH' if kind == 'pointer' else ' DIFFERENT relocs '
    if diagnostic not in verify:
        raise ValueError('missing %s mutation diagnostic' % kind)
    return kind


def check_library_consistency(positive, controls, expected_sha256=None):
    runs = [('positive', positive)] + [('control %d' % (i + 1), c) for i, c in enumerate(controls)]
    configs = [(label, run.get('provenance', {}).get('library_overlay')) for label, run in runs]
    active = [c for _, c in configs if isinstance(c, dict) and c.get('enabled') is True]
    if not active and expected_sha256 is None:
        return []
    if not active:
        return ['library overlay expected but not recorded']
    first = active[0]; errors = []
    index_metadata = any('section_index_base' in c or 'reader_sha256' in c for c in active)
    if expected_sha256 is not None and (re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256) is None or first.get('selection_sha256') != expected_sha256.lower()):
        errors.append('library selection digest mismatch')
    for label, c in configs:
        if not isinstance(c, dict) or c.get('enabled') is not True:
            errors.append(label + ': library overlay mode missing or disabled'); continue
        if not isinstance(c.get('selection_sha256'), str) or re.fullmatch(r'[0-9a-f]{64}', c['selection_sha256']) is None:
            errors.append(label + ': invalid library selection digest')
        if c.get('selection_sha256') != first.get('selection_sha256') or c.get('archive_sha256') != first.get('archive_sha256') or c.get('selected') != first.get('selected') or c.get('bytes') != first.get('bytes'):
            errors.append(label + ': library provenance mismatch')
        if index_metadata:
            if type(c.get('section_index_base')) is not int or c['section_index_base'] not in (0, 1):
                errors.append(label + ': invalid library section index base')
            if not isinstance(c.get('reader_sha256'), str) or re.fullmatch(r'[0-9a-f]{64}', c['reader_sha256']) is None:
                errors.append(label + ': missing or invalid library reader hash')
            if c.get('section_index_base') != first.get('section_index_base') or c.get('reader_sha256') != first.get('reader_sha256'):
                errors.append(label + ': library section reader/index mode mismatch')
        archives=c.get('archive_sha256')
        if not isinstance(archives,dict) or set(archives) != {'libcmt.lib','libcpmt.lib'} or any(not isinstance(v,str) or re.fullmatch(r'[0-9a-f]{64}',v) is None for v in archives.values()):
            errors.append(label + ': invalid library archive hashes')
        if type(c.get('selected')) is not int or c['selected'] <= 0 or type(c.get('bytes')) is not int or c['bytes'] <= 0:
            errors.append(label + ': invalid library coverage counts')
    return errors


def check_weak_consistency(positive, controls):
    """If any run records weak mode, require matching mode and tool hashes."""
    runs = [('positive', positive)] + [('control %d' % (i + 1), c) for i, c in enumerate(controls)]
    configs = [(label, run.get('provenance', {}).get('weak_coff')) for label, run in runs]
    if not any(isinstance(c, dict) and c.get('enabled') is True for _, c in configs):
        return []  # Backward compatible with archived pre-feature evidence.
    first = next(c for _, c in configs if isinstance(c, dict) and c.get('enabled') is True)
    return [error for label, run in runs for error in check_weak_coff(
        run, label, '1', first.get('helper_sha256'), first.get('resolver_sha256'))]


def check_weak_coff(run, label, expected, helper_sha256, resolver_sha256):
    errors = []
    config = run.get('provenance', {}).get('weak_coff')
    if not isinstance(config, dict) or config.get('enabled') is not (expected == '1'):
        errors.append(label + ': weak COFF mode missing or mismatched')
        return errors
    if expected == '1':
        for key, value in (('helper_sha256', helper_sha256), ('resolver_sha256', resolver_sha256)):
            if not isinstance(value, str) or re.fullmatch(r'[0-9a-fA-F]{64}', value) is None or config.get(key) != value.lower():
                errors.append(label + ': weak COFF ' + key + ' mismatch')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--positive', required=True, type=Path)
    parser.add_argument('--default', required=True, type=Path, help='legacy non-M3 comparison baseline; use FNV_M3=0 after default promotion')
    parser.add_argument('--control', required=True, action='append', type=Path)
    parser.add_argument('--verdict', required=True, type=Path)
    parser.add_argument('--check-control-logs', action='store_true', help='check Batch 7 or 8 control logs named by each summary')
    parser.add_argument('--require-cell-state', action='store_true', help='require recorded cell change and quickload restoration')
    parser.add_argument('--require-extended-mode', action='store_true', help='require M3, DV1 and extended-mode recorded evidence')
    parser.add_argument('--expected-selection', help='require this exact recorded M3 selection')
    parser.add_argument('--expected-control', action='append', help='require this control identifier, in summary order (repeat for each control)')
    parser.add_argument('--expected-selection-sha256', help='require this recorded selection SHA-256')
    parser.add_argument('--expected-weak-coff', choices=('0', '1'))
    parser.add_argument('--expected-weak-helper-sha256')
    parser.add_argument('--expected-weak-resolver-sha256')
    parser.add_argument('--expected-library-sha256')
    args = parser.parse_args()
    if (args.expected_selection is None) != (args.expected_control is None):
        parser.error('--expected-selection and --expected-control must be supplied together')
    if args.expected_weak_coff == '1' and not (args.expected_weak_helper_sha256 and args.expected_weak_resolver_sha256):
        parser.error('weak mode 1 requires helper and resolver digests')
    if args.expected_weak_coff != '1' and (args.expected_weak_helper_sha256 or args.expected_weak_resolver_sha256):
        parser.error('weak digests require --expected-weak-coff 1')
    try:
        def read(path):
            return json.loads(path.read_text(encoding='utf-8-sig'))
        controls = [read(p) for p in args.control]
        positive = read(args.positive)
        default = read(args.default)
        errors = check(positive, default, controls, read(args.verdict))
        errors.extend(check_weak_consistency(positive, controls))
        errors.extend(check_library_consistency(positive, controls, args.expected_library_sha256))
        if args.expected_weak_coff is not None:
            for label, run in [('positive', positive)] + [('control %d' % (i + 1), c) for i, c in enumerate(controls)]:
                errors.extend(check_weak_coff(run, label, args.expected_weak_coff, args.expected_weak_helper_sha256, args.expected_weak_resolver_sha256))
        if args.require_cell_state:
            errors.extend(check_cell_state(read(args.verdict)))
        if args.expected_selection_sha256 is not None:
            errors.extend(check_selection_sha256(positive, controls, args.expected_selection_sha256))
        if args.expected_selection is not None:
            errors.extend(check_recorded_config(positive, default, controls, args.expected_selection, args.expected_control))
        if args.require_extended_mode:
            errors.extend(check_extended_mode(positive, 'positive'))
            errors.extend(check_provenance(positive, [('default', default)] + [('control %d' % (i + 1), run) for i, run in enumerate(controls)]))
            for i, control in enumerate(controls):
                errors.extend(check_extended_mode(control, 'control %d' % (i + 1)))
        if args.check_control_logs:
            kinds = [check_control_logs(p, run) for p, run in zip(args.control, controls)]
            if set(kinds) != {'value', 'pointer'}:
                errors.append('control logs must identify at least one value and one pointer mutation')
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print('ERROR: cannot parse saved evidence:', exc, file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print('FAIL:', error)
        return 1
    print('PASS: saved hashes, control markers, and extended harness evidence agree')
    if args.check_control_logs:
        print('PASS: saved logs identify value and pointer controls with expected failure diagnostics')
    else:
        print('LIMIT: summary markers alone do not identify the mutations')
    if args.require_extended_mode:
        print('PASS: extended mode and matching code/field-count provenance recorded')
        print('LIMIT: selection file contents and relocation-table byte identity are not established')
    if args.expected_selection is not None:
        print('PASS: recorded M3 selection and control identifiers match expectations')
        print('LIMIT: recorded identifiers do not independently establish the applied inputs or mutations')
    if args.expected_selection_sha256 is not None:
        print('PASS: recorded selection SHA-256 values match the expected digest')
        print('LIMIT: selection file contents were not independently checked')
    print('LIMIT: saved evidence was not independently rerun')
    return 0


if __name__ == '__main__':
    sys.exit(main())
