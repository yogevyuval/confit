import os

import click
from jinja2 import Template

from confit.backends.ssm import SsmBackend


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
def generate_config(region, prefix, input_template, output):
    ssm = SsmBackend(region)

    if not os.path.exists(input_template):
        raise TemplateNotFoundException('Template {} not found'.format(input_template))

    result = render_params(input_template.read(), prefix, ssm)
    print(result)

    if output:
        with open(output, 'w') as f:
            f.write(result)


def render_params(input_template, prefix, ssm):
    vars, prefixed_vars = ssm.get_parameters(prefix)

    tm = Template(input_template)
    result = tm.render(vars=Vars(vars), prefixed_vars=Vars(prefixed_vars))
    return result


if __name__ == '__main__':
    generate_config()
