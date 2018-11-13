from cfn_resource_provider import ResourceProvider
from botocore.exceptions import ClientError
import boto3
import logging
import os

log = logging.getLogger()
log.setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))

client = boto3.client('apigateway')


class EnableStageTracingProvider(ResourceProvider):
    def __init__(self):
        super(EnableStageTracingProvider, self).__init__()
        self.request_schema = {
            'type': 'object',
            'required': ['RestApiId', 'StageName'],
            'properties': {
                'RestApiId': {'type': 'string'},
                'StageName': {'type': 'string'}
            }
        }

    def create(self):
        try:
            updates = {'restApiId': self.properties['RestApiId'], 'stageName': self.properties['StageName']}

            patch_operations = {
                'patchOperations': [{
                    'op': 'replace',
                    'path': '/tracingEnabled',
                    'value': True
                }]
            }

            updates.update(patch_operations)
            response = client.update_stage(**updates)
            self.physical_resource_id = response['deploymentId'] + response['stageName']

            self.success(response)
        except ClientError as error:
            self.physical_resource_id = 'failed-to-create'
            self.fail(f'{error}')

    def update(self):
        if self.properties['tracingEnabled'] is True:
            self.delete()
            self.create()
        else:
            self.delete()

    def delete(self):
        try:
            updates = {'restApiId': self.properties['RestApiId'], 'stageName': self.properties['StageName']}

            patch_operations = {
                'patchOperations': [{
                    'op': 'replace',
                    'path': '/tracingEnabled',
                    'value': False
                }]
            }

            updates.update(patch_operations)
            response = client.update_stage(**updates)

            self.success(response)
        except ClientError as error:
            self.fail(f'{error}')


provider = EnableStageTracingProvider()


def handler(request, context):
    return provider.handle(request, context)
