"""Resolve M3 build-driver environment without changing the input mapping."""

import os

DEFAULT_SELECTION = 'phase2/selection.json'
DEFAULT_SELECTION_SHA256 = '08b8740c57eab56aaf8a861a68cd9ed3cc5aa6bccdd6ca81283b05081a651b81'
DEFAULT_LIBRARY_SELECTION = 'phase2/library_candidates.json'
DEFAULT_LIBRARY_SHA256 = '74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700'
_M3_ROOT = os.path.dirname(os.path.abspath(__file__))


def _selection_path(value):
    return os.path.normcase(os.path.abspath(os.path.join(_M3_ROOT, value)))


def configure(environment, promoted=False):
    """Return effective child environment; promotion is disabled unless requested.

    Empty values are treated as unset. DV_M3 and DV3_SKIP are internal derived
    flags: the driver must set them after producing the corresponding artifacts.
    """
    env = dict(environment)
    keys = ('FNV_M3', 'FNV_M3_SEL', 'FNV_M3_DV1', 'FNV_M3_DV1_EXT', 'FNV_M3_RTTI_NAME_LITERAL')
    for key in keys:
        if env.get(key) == '':
            env.pop(key, None)
    # Never inherit paths or mode markers derived by an earlier build.
    env.pop('DV_M3', None)
    env.pop('DV3_SKIP', None)
    if promoted:
        env.setdefault('FNV_M3', '1')
    if env.get('FNV_M3') != '1':
        for key in list(env):
            if key.startswith('FNV_M3_'):
                env.pop(key)
        return env
    if promoted:
        env.setdefault('FNV_M3_SEL', DEFAULT_SELECTION)
        env.setdefault('FNV_M3_DV1', '1')
    if env.get('FNV_M3_DV1') == '1':
        if promoted:
            env.setdefault('FNV_M3_DV1_EXT', '1')
    else:
        for key in ('FNV_M3_DV1_EXT', 'FNV_M3_DV1_KINDS', 'FNV_M3_DV1_OUT', 'FNV_M3_RTTI_NAME_LITERAL'):
            env.pop(key, None)
    toggle = env.get('FNV_M3_LIB')
    explicit_library = ('FNV_M3_LIB_SELECTION' in environment or 'FNV_M3_LIB_SHA256' in environment)
    default_selected = _selection_path(env.get('FNV_M3_SEL', DEFAULT_SELECTION)) == _selection_path(DEFAULT_SELECTION)
    if (promoted and default_selected and env.get('FNV_M3_DV1') == '1'
            and env.get('FNV_M3_DV1_EXT') == '1'
            and not env.get('FNV_M3_DV1_KINDS') and not env.get('FNV_M3_DV1_OUT')):
        env.setdefault('FNV_M3_RTTI_NAME_LITERAL', '1')
    if (promoted or toggle == '1') and env.get('FNV_M3_DV1') == '1' and toggle != '0' and not explicit_library and (toggle == '1' or default_selected):
        env['FNV_M3_LIB_SELECTION'] = os.path.abspath(os.path.join(_M3_ROOT, DEFAULT_LIBRARY_SELECTION))
        env['FNV_M3_LIB_SHA256'] = DEFAULT_LIBRARY_SHA256
    return env


def validate_driver_options(env, skip_data_v1=False, raw_environment=None):
    """Reject driver settings that would reuse stale DV1 snapshot artifacts."""
    raw = env if raw_environment is None else raw_environment
    toggle = raw.get('FNV_M3_LIB') or None
    if toggle not in (None, '0', '1'):
        raise ValueError('FNV_M3_LIB must be 0 or 1')
    selection, digest = raw.get('FNV_M3_LIB_SELECTION'), raw.get('FNV_M3_LIB_SHA256')
    if toggle == '0' and (selection is not None or digest is not None):
        raise ValueError('FNV_M3_LIB=0 conflicts with explicit library selection')
    if toggle == '1' and (env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1):
        raise ValueError('library overlay requires active M3/DV1 and fresh data-v1')
    if selection is not None or digest is not None:
        import re
        if not selection or not digest or re.fullmatch(r'[0-9a-fA-F]{64}', digest) is None:
            raise ValueError('library overlay requires selection and a SHA-256 digest')
        if env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1:
            raise ValueError('library overlay requires active M3/DV1 and fresh data-v1')
    index_mode = raw.get('FNV_DV1_LIB_COFF_INDEX_V2') or '0'
    if index_mode not in ('0', '1'):
        raise ValueError('FNV_DV1_LIB_COFF_INDEX_V2 must be 0 or 1')
    if index_mode == '1':
        if env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1:
            raise ValueError('one-based library mode requires active M3/DV1 and fresh data-v1')
        if not selection or not digest or toggle == '0':
            raise ValueError('one-based library mode requires an explicit compatible library selection and SHA-256')
        if _selection_path(selection) == _selection_path(DEFAULT_LIBRARY_SELECTION):
            raise ValueError('default library selection uses legacy section indices')
    weak = env.get('FNV_COFF_WEAK', '0')
    if weak not in ('0', '1'):
        raise ValueError('FNV_COFF_WEAK must be 0 or 1')
    if weak == '1' and skip_data_v1:
        raise ValueError('weak COFF mode requires a fresh data-v1 run')
    if env.get('FNV_M3') == '1' and env.get('FNV_M3_DV1') == '1':
        if skip_data_v1:
            raise ValueError('M3 DV1 requires data-v1; --skip-data-v1 would reuse stale artifacts')
        if env.get('FNV_M3_DV1_OUT'):
            raise ValueError('M3 DV1 diagnostic output redirect is incompatible with the build driver')


def validate_library_result(result, selection_sha256):
    """Validate fresh DV1 library provenance before recording it."""
    import re
    if not isinstance(result, dict) or result.get('selection_sha256') != selection_sha256:
        raise ValueError('missing or mismatched library overlay provenance')
    archives = result.get('archive_sha256')
    if not isinstance(archives, dict) or set(archives) != {'libcmt.lib', 'libcpmt.lib'}:
        raise ValueError('missing library archive hashes')
    if any(not isinstance(v, str) or re.fullmatch(r'[0-9a-f]{64}', v) is None for v in archives.values()):
        raise ValueError('invalid archive hashes')
    if type(result.get('selected')) is not int or result['selected'] <= 0 or type(result.get('bytes')) is not int or result['bytes'] <= 0:
        raise ValueError('invalid library selected/byte counts')
    return dict(archive_sha256=dict(archives), selected=result['selected'], bytes=result['bytes'])
