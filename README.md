# ApiGateway Custom Provider for X-Ray Support

Recently the AWS [API Gateway](https://aws.amazon.com/about-aws/whats-new/2018/09/amazon-api-gateway-adds-support-for-aws-x-ray/) 
received support for AWS X-Ray. However, there is, as of yet, no CloudFormation support to enable this feature. By adding
this custom resource to your template we enable X-Ray tracing for the specified API and stage combination.

##  What is X-Ray?
   
[X-Ray](https://aws.amazon.com/xray/) enables us to trace requests as they are routed and processed in the cloud. 

## How do I use it?

Checkout the sample rules in the [demo-stack.yaml](cloudformation/demo-stack.yaml) for more information.

## Syntax YAML

```yaml
Type: Custom::EnableStageTracing
Properties:
  RestApiId: Id of the api
  StageName: Name of the stage for which to enable x-ray tracing
  ServiceToken: Arn of the custom resource provider lambda function
```

## Installation

To install this custom resource follow these steps:

- Package the Lambda using docker and upload it to S3 using ```make deploy``` (See the [makefile](Makefile) for more info)

- Deploy the cfn-apigateway-provider stack using ```make deploy-provider``` or 
type (remember to fill in your bucket name and key): 

```sh
aws cloudformation create-stack \
	--capabilities CAPABILITY_IAM \
	--stack-name cfn-apigateway-provider \
	--template-body file://cloudformation/cfn-apigateway-provider.yaml
	--parameters \
                ParameterKey=S3BucketPrefix,ParameterValue=INSERT_BUCKET_NAME_HERE \
                ParameterKey=CFNCustomProviderZipFileName,ParameterValue=INSERT_BUCKET_KEY_HERE 

aws cloudformation wait stack-create-complete  --stack-name cfn-apigate-way-provider
```

## Demo

To try out the custom resource type the following to deploy the demo:

```sh
aws cloudformation create-stack --stack-name cfn-apigateway-provider-demo \
	--template-body file://cloudformation/demo-stack.yaml \
aws cloudformation wait stack-create-complete  --stack-name cfn-apigateway-provider-demo
```

This will deploy a cfn-apigateway-provider demo stack containing an apigateway with a 'hello world' lambda function  on 
the path '/hello' and also deploy the custom resource to enable x-ray tracing on the stage 'demo'.