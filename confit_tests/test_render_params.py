import pytest

from confit.main import render_params, VarKeyNotFound


def stub_params():
    return {'/some_prefix/some/var': 'testing!', '/global/var': 'global value'}, {'/some/var': 'testing!'}


def test_global_var():
    vars, prefixed_vars = stub_params()
    results = render_params("{{vars.get('/global/var')}}", vars, prefixed_vars)
    assert results == 'global value'


def test_prefixed_var():
    vars, prefixed_vars = stub_params()
    results = render_params("{{prefixed_vars.get('/some/var')}}", vars, prefixed_vars)
    assert results == 'testing!'


def test_default_value():
    vars, prefixed_vars = stub_params()
    results = render_params("{{prefixed_vars.get('/wierd/var', 'default value!')}}", vars, prefixed_vars)
    assert results == 'default value!'


def test_get_var_with_get_item():
    vars, prefixed_vars = stub_params()
    results = render_params("{{prefixed_vars['/some/var']}}", vars, prefixed_vars)
    assert results == 'testing!'


def test_unknown_var_get_item():
    vars, prefixed_vars = stub_params()
    with pytest.raises(VarKeyNotFound):
        render_params("{{prefixed_vars['/wierd/var']}}", vars, prefixed_vars)


def test_unknown_var_get():
    vars, prefixed_vars = stub_params()
    results = render_params("{{prefixed_vars.get('/wierd/var')}}", vars, prefixed_vars)
    assert results == ''


def test_empty_prefix_prefixed_vars():
    vars, prefixed_vars = stub_params()
    results = render_params("{{prefixed_vars.get('/some/var')}}", vars, prefixed_vars)
    assert results == 'testing!'
