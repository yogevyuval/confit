import boto3

PATH_SEP = '/'


class SsmBackend:
    def __init__(self, region):
        self.session = boto3.session.Session()
        self.client = self.session.client(service_name='ssm', region_name=region)
        pass

    def get_parameters(self, prefix):
        vars = {}
        prefixed_vars = {}

        aws_params = self.client.get_parameters_by_path(Path=PATH_SEP, Recursive=True, WithDecryption=True)

        for p in aws_params['Parameters']:
            vars[p['Name']] = p['Value']
            if p['Name'].startswith(prefix):
                prefixed_vars[p['Name'].replace(prefix, '')] = p['Value']

        return vars, prefixed_vars
