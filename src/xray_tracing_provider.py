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
        self.physical_resource_id = self.properties['RestApiId'] + self.properties['StageName']
        self.set_tracing(self.properties['RestApiId'], self.properties['StageName'], True)

    def update(self):
        self.set_tracing(self.old_properties['RestApiId'], self.old_properties['StageName'], False)
        self.set_tracing(self.properties['RestApiId'], self.properties['StageName'], True)

    def delete(self):
        self.set_tracing(self.properties['RestApiId'], self.properties['StageName'], False)

    def set_tracing(self, api_id, stage_name, tracing_enabled: bool):
        try:
            updates = {'restApiId': api_id, 'stageName': stage_name}

            patch_operations = {
                'patchOperations': [{
                    'op': 'replace',
                    'path': '/tracingEnabled',
                    'value': f'{tracing_enabled}'
                }]
            }

            updates.update(patch_operations)
            response = client.update_stage(**updates)

            self.success(f'{response}')
        except ClientError as error:
            self.fail(f'{error}')


provider = EnableStageTracingProvider()


def handler(request, context):
    return provider.handle(request, context)
