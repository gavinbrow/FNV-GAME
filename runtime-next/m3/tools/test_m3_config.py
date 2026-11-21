"""Run with python -I runtime-next/m3/tools/test_m3_config.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import configure, validate_driver_options, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256, DEFAULT_LIBRARY_SELECTION, DEFAULT_LIBRARY_SHA256


def test_defaults():
    assert configure({}) == {}
    assert configure({}, promoted=True) == {
        'FNV_M3': '1', 'FNV_M3_SEL': DEFAULT_SELECTION,
        'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '1', 'FNV_M3_RTTI_NAME_LITERAL': '1',
        'FNV_M3_LIB_SELECTION': str(Path(__file__).resolve().parents[1] / DEFAULT_LIBRARY_SELECTION),
        'FNV_M3_LIB_SHA256': DEFAULT_LIBRARY_SHA256}
    assert len(DEFAULT_SELECTION_SHA256) == 64


def test_legacy_and_disabled_cleanup():
    source = {'FNV_M3': '0', 'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '1',
              'FNV_M3_SEL': 'stale.json', 'FNV_M3_NEGCTL': 'b8v',
              'FNV_M3_DV1_KINDS': 'rtti', 'FNV_M3_DV1_OUT': 'diagnostic',
              'DV_M3': '1', 'DV3_SKIP': 'stale.json', 'OTHER': 'keep'}
    original = dict(source)
    for promoted in (False, True):
        assert configure(source, promoted) == {'FNV_M3': '0', 'OTHER': 'keep'}
    assert source == original
    assert configure({'FNV_M3': '1'}) == {'FNV_M3': '1'}


def test_explicit_overrides():
    source = {'FNV_M3': '1', 'FNV_M3_SEL': 'custom.json', 'FNV_M3_DV1': '0',
              'FNV_M3_DV1_EXT': '1', 'DV_M3': '1', 'DV3_SKIP': 'old.json'}
    assert configure(source, True) == {'FNV_M3': '1', 'FNV_M3_SEL': 'custom.json', 'FNV_M3_DV1': '0'}
    assert configure({'FNV_M3': '1', 'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '0'}, True) == {
        'FNV_M3': '1', 'FNV_M3_SEL': DEFAULT_SELECTION, 'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '0',
        'FNV_M3_LIB_SELECTION': str(Path(__file__).resolve().parents[1] / DEFAULT_LIBRARY_SELECTION),
        'FNV_M3_LIB_SHA256': DEFAULT_LIBRARY_SHA256}
    assert configure({'FNV_M3_DV1_EXT': '1'}) == {}
    assert configure({'FNV_M3': '1', 'FNV_M3_DV1': '0', 'FNV_M3_DV1_KINDS': 'rtti',
                      'FNV_M3_DV1_OUT': 'diagnostic'}) == {'FNV_M3': '1', 'FNV_M3_DV1': '0'}
    assert configure({'FNV_M3': '1', 'FNV_M3_DV1': '1', 'FNV_M3_DV1_KINDS': 'rtti'}) == {
        'FNV_M3': '1', 'FNV_M3_DV1': '1', 'FNV_M3_DV1_KINDS': 'rtti'}


def test_empty_values_and_input_copy():
    source = {'FNV_M3': '', 'FNV_M3_SEL': '', 'FNV_M3_DV1': '', 'FNV_M3_DV1_EXT': '', 'OTHER': ''}
    assert configure(source, True) == dict(configure({}, True), OTHER='')
    assert configure(source) == {'OTHER': ''}
    assert source['FNV_M3'] == ''
    assert configure(source) is not source


def test_driver_options():
    active = configure({}, True)
    for env, skip in ((active, True), (dict(active, FNV_M3_DV1_OUT='redirect'), False)):
        try:
            validate_driver_options(env, skip_data_v1=skip)
        except ValueError:
            pass
        else:
            raise AssertionError('unsafe driver settings accepted')
    validate_driver_options(active)
    validate_driver_options(dict(active, FNV_M3_DV1_KINDS='rtti'))
    validate_driver_options({'FNV_M3': '0', 'FNV_M3_DV1': '1', 'FNV_M3_DV1_OUT': 'redirect'}, True)
    validate_driver_options({'FNV_M3': '1', 'FNV_M3_DV1': '0', 'FNV_M3_DV1_OUT': 'redirect'}, True)


def test_rtti_literal_promotion_scope():
    assert configure({}, True)['FNV_M3_RTTI_NAME_LITERAL'] == '1'
    assert configure({'FNV_M3_RTTI_NAME_LITERAL': ''}, True)['FNV_M3_RTTI_NAME_LITERAL'] == '1'
    assert configure({'FNV_M3_RTTI_NAME_LITERAL': '0'}, True)['FNV_M3_RTTI_NAME_LITERAL'] == '0'
    assert 'FNV_M3_RTTI_NAME_LITERAL' not in configure({'FNV_M3':'0','FNV_M3_RTTI_NAME_LITERAL':'1'}, True)
    assert 'FNV_M3_RTTI_NAME_LITERAL' not in configure({'FNV_M3_DV1':'0','FNV_M3_RTTI_NAME_LITERAL':'1'}, True)
    for overrides in ({'FNV_M3_SEL':'custom.json'}, {'FNV_M3_DV1':'0'}, {'FNV_M3_DV1_EXT':'0'}, {'FNV_M3_DV1_KINDS':'rtti'}, {'FNV_M3_DV1_OUT':'diagnostic'}):
        assert 'FNV_M3_RTTI_NAME_LITERAL' not in configure(overrides, True)
    assert 'FNV_M3_RTTI_NAME_LITERAL' not in configure({'FNV_M3':'1','FNV_M3_DV1':'1','FNV_M3_DV1_EXT':'1'})
    assert configure({'FNV_M3_SEL':'custom.json','FNV_M3_RTTI_NAME_LITERAL':'1'}, True)['FNV_M3_RTTI_NAME_LITERAL'] == '1'


if __name__ == '__main__':
    for name, test in list(globals().items()):
        if name.startswith('test_') and callable(test):
            test()
            print('PASS', name)
