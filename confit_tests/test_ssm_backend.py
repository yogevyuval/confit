import pytest

from confit.backends.ssm import Param, SsmBackend, parse_aws_response
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
    result = parse_aws_response(stub_response())
    assert result == [Param('/production/list/param1', 'param1'), Param('/production/list/param2', 'param2'), Param('/dev/list/param1', 'devparam1')]
