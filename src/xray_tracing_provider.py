from cfn_resource_provider import ResourceProvider
from botocore.exceptions import ClientError
import boto3
import logging
import os

log = logging.getLogger()
log.setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))

client = boto3.client('apigateway')


class XrayTracingProvider(ResourceProvider):
    def __init__(self):
        super(XrayTracingProvider, self).__init__()
        self.request_schema = {
            'type': 'object',
            'required': ['RestApiId', 'StageName'],
            'properties': {
                'RestApiId': {'type': 'string'},
                'StageName': {'type': 'string'}
            }
        }

    def create(self):
        kwargs = self.properties.copy()

        try:
            kwargs.pop('ServiceToken', None)

            patch_operations=[
                {
                    'op': 'add',
                    'path': '/tracingEnabled',
                    'value': 'True'
                },
            ]

            kwargs.update('patchOperations', patch_operations)
            response = client.update_stage(kwargs)
            self.physical_resource_id = response['deploymentId']

            self.success(response)
        except ClientError as error:
            self.fail(error)

    def update(self):
        if self.properties['tracingEnabled'] is True:
            self.delete()
            self.create()
        else:
            self.delete()

    def delete(self):
        kwargs = self.properties.copy()

        try:
            kwargs.pop('ServiceToken', None)

            patch_operations=[
                {
                    'op': 'remove',
                    'path': '/tracingEnabled'
                },
            ]

            kwargs.update('patchOperations', patch_operations)
            response = client.update_stage(kwargs)

            self.success(response)
        except ClientError as error:
            self.fail(error)


provider = XrayTracingProvider()


def handler(request, context):
    return provider.handle(request, context)
