import os
from typing import Dict, List

import click
from jinja2 import Template

from confit.backends.ssm import SsmBackend, Param


class TemplateNotFoundException(Exception):
    pass


class VarKeyNotFound(Exception):
    pass


class Vars:
    def __init__(self, vars):
        self._vars = vars

    def get(self, name, default=''):
        return self._vars.get(name, default)

    def __getitem__(self, item):
        if item not in self._vars:
            raise VarKeyNotFound('Could not find {0} in {1}'.format(item, self._vars))

        return self._vars[item]


@click.command()
@click.option('--region', prompt='Your region', default='us-east-1', help='The region of your SSM')
@click.option('--prefix', default='', help='prefix to create prefixed_vars')
@click.option('--input-template', '-i', required=True, help='Path to your template')
@click.option('--output', '-o', help='Output path')
def generate_config(region: str, prefix: str, input_template: str, output: str):

    if not os.path.exists(input_template):
        raise TemplateNotFoundException('Template {} not found'.format(input_template))

    ssm = SsmBackend(region)
    parameters: List[Param] = ssm.get_parameters()

    vars, prefixed_vars = build_vars(parameters, prefix)

    result = render_params(open(input_template).read(), vars, prefixed_vars)
    print(result)

    if output:
        with open(output, 'w') as f:
            f.write(result)


def build_vars(parameters: List[Param], prefix: str):
    vars = {}
    prefixed_vars = {}

    for p in parameters:
        vars[p.name] = p.value
        if p.name.startswith(prefix):
            prefixed_vars[p.name.replace(prefix, '')] = p.value

    return vars, prefixed_vars


def render_params(input_template: str, vars: Dict[str, str], prefixed_vars: Dict[str, str]) -> str:
    tm = Template(input_template)
    result = tm.render(vars=Vars(vars), prefixed_vars=Vars(prefixed_vars))
    return result


if __name__ == '__main__':
    generate_config()
