from typing import List, Dict

import boto3

PATH_SEP = '/'


class Param:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


def parse_aws_response(response: Dict):
    return list(map(lambda p: Param(p['Name'], p['Value']), response['Parameters']))


class SsmBackend:
    def __init__(self, region):
        self.session = boto3.session.Session()
        self.client = self.session.client(service_name='ssm', region_name=region)

    def request(self):
        return self.client.get_parameters_by_path(Path=PATH_SEP, Recursive=True, WithDecryption=True)

    def get_parameters(self) -> List[Param]:
        return parse_aws_response(self.request())
