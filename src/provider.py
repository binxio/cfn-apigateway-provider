import xray_tracing_provider


def handler(request, context):
    if request['ResourceType'] == 'Custom::EnableStageTracing':
        return xray_tracing_provider.handler(request, context)
    else:
        print(f"Unknown resource type: {request['ResourceType']}")
