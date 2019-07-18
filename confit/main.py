import os

import boto3
import click
from jinja2 import Template

PATH_SEP = '/'


class TemplateNotFoundException(Exception):
    pass


class VarKeyNotFound(Exception):
    pass


class Vars(object):
    def __init__(self, vars):
        self._vars = vars

    def get(self, name, default=''):
        return self._vars.get(name, default)

    def __getitem__(self, item):
        if item not in self._vars:
            raise VarKeyNotFound(f'Could not find {item} in {self._vars}')

        return self._vars[item]


@click.command()
@click.option('--region', prompt='Your region', default='us-east-1', help='The region of your SSM')
@click.option('--prefix', default='', help='prefix to create prefixed_vars')
@click.option('--input-template', '-i', help='Path to your template')
@click.option('--output', '-o', help='Output path')
def generate_config(region, prefix, input_template, output):
    session = boto3.session.Session()
    client = session.client(service_name='ssm', region_name=region)

    vars = {}
    prefixed_vars = {}

    aws_params = client.get_parameters_by_path(Path=PATH_SEP, Recursive=True, WithDecryption=True)

    for p in aws_params['Parameters']:
        vars[p['Name']] = p['Value']
        if p['Name'].startswith(prefix):
            prefixed_vars[p['Name'].replace(prefix, '')] = p['Value']

    if not os.path.exists(input_template):
        raise TemplateNotFoundException(f'Template {input_template} not found')

    tm = Template(open(input_template).read())

    result = tm.render(vars=Vars(vars), prefixed_vars=Vars(prefixed_vars))
    print(result)

    if output:
        with open(output, 'w') as f:
            f.write(result)


if __name__ == '__main__':
    generate_config()
