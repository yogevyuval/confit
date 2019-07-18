from typing import List

import boto3

PATH_SEP = '/'


class Param:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class SsmBackend:
    def __init__(self, region):
        self.session = boto3.session.Session()
        self.client = self.session.client(service_name='ssm', region_name=region)

    def request(self):
        return self.client.get_parameters_by_path(Path=PATH_SEP, Recursive=True, WithDecryption=True)

    def get_parameters(self) -> List[Param]:
        aws_params = self.request()
        return aws_params['Parameters'].map(lambda p: Param(p['Name'], p['Value']))
