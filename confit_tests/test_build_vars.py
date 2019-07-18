import pytest

from confit.backends.ssm import Param
from confit.main import build_vars


def stub_params():
    return [Param('/production/list/param1', 'value1'), Param('/production/list/param2', 'value2'),
            Param('/production/list/param3', 'value3'), Param('/dev/list/param4', 'value4')]


def test_prefix():
    vars, prefixed_vars = build_vars(stub_params(), '/production')
    assert vars == {'/production/list/param1': 'value1', '/production/list/param2': 'value2',
                    '/production/list/param3': 'value3',
                    '/dev/list/param4': 'value4'}

    assert prefixed_vars == {'/list/param1': 'value1', '/list/param2': 'value2',
                             '/list/param3': 'value3'}


def test_empty_prefix():
    vars, prefixed_vars = build_vars(stub_params(), '')
    assert vars == {'/production/list/param1': 'value1', '/production/list/param2': 'value2',
                    '/production/list/param3': 'value3',
                    '/dev/list/param4': 'value4'}

    assert prefixed_vars == vars
