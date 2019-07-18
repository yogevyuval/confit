import pytest

from confit.backends.ssm import Param, SsmBackend
from confit.main import build_vars


def stub_response():
    return {
        "Parameters": [
            {
                "Name": "/production/list/param1",
                "Value": "param1",
            },
            {
                "Name": "/production/list/param2",
                "Value": "param2",
            },
            {
                "Name": "/dev/list/param1",
                "Value": "devparam1",
            }
        ]
    }


def test_get_parameters():
    pass
