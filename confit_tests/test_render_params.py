import pytest

from confit.main import render_params, VarKeyNotFound


class SsmStub:
    def get_parameters(self, prefix):
        return {'/some_prefix/some/var': 'testing!', '/global/var': 'global value'}, {'/some/var': 'testing!'}


def test_global_var():
    results = render_params("{{vars.get('/global/var')}}", '/some_prefix', SsmStub())
    assert results == 'global value'


def test_prefixed_var():
    results = render_params("{{prefixed_vars.get('/some/var')}}", '/some_prefix', SsmStub())
    assert results == 'testing!'


def test_default_value():
    results = render_params("{{prefixed_vars.get('/wierd/var', 'default value!')}}", '/some_prefix', SsmStub())
    assert results == 'default value!'


def test_get_var_with_get_item():
    results = render_params("{{prefixed_vars['/some/var']}}", '/some_prefix', SsmStub())
    assert results == 'testing!'


def test_unknown_var_get_item():
    with pytest.raises(VarKeyNotFound):
        render_params("{{prefixed_vars['/wierd/var']}}", '/some_prefix', SsmStub())


def test_unknown_var_get():
    results = render_params("{{prefixed_vars.get('/wierd/var')}}", '/some_prefix', SsmStub())
    assert results == ''


def test_empty_prefix():
    results = render_params("{{vars.get('/some/var')}}", '', SsmStub())
    assert results == 'testing!'


def test_empty_prefix_prefixed_vars():
    results = render_params("{{prefixed_vars.get('/some/var')}}", '', SsmStub())
    assert results == 'testing!'
