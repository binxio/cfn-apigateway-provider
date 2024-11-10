Deprecated Nov 2024  -> supported by [AWS::ApiGateway::Stage](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tracingenabled)

# ApiGateway Custom Provider for X-Ray Support

Recently the AWS [API Gateway](https://aws.amazon.com/about-aws/whats-new/2018/09/amazon-api-gateway-adds-support-for-aws-x-ray/) 
received support for AWS X-Ray. However, there is, as of yet, no CloudFormation support to enable this feature on API Gateway. 
By adding this custom resource to your template we can enable X-Ray tracing for the specified API and stage combination.

##  What is X-Ray and why do I want it?
   
[X-Ray](https://aws.amazon.com/xray/) is a distributed tracing system that enables us to analyze and debug distributed 
applications. This is extremely useful for serverless applications which make use of many components such as
API Gateway, Lambda, DynamoDB, etc. Since the API Gateway is a central point for these applications enabling X-Ray here
is extremely valuable. However, since we believe in infrastructure as code we do not want to use the AWS Console or 
API calls to manually enable this feature. Instead we want to simply define this property in our CloudFormation template.
This resource allows us to do just that!

## How do I use it?

Deploy the custom resource as described in the installation section. Next add the custom resource to your 
CloudFormation template, specify the desired API and stage, and deploy.

Checkout the sample rules in the [demo-stack.yaml](cloudformation/demo-stack.yaml) for more information.

## Syntax YAML

```yaml
Type: Custom::EnableStageTracing
Properties:
  RestApiId: Id of the api
  StageName: Name of the stage for which to enable x-ray tracing
  ServiceToken: Arn of the custom resource provider lambda function
```

*Note*: The stage must exist before this resource is created. To enforce this use 
[DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) to ensure 
the tracing isn't enabled until after the stage after has been created.

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

To try out the custom resource first make sure you have the [sam-cli](https://github.com/awslabs/aws-sam-cli/blob/develop/docs/installation.rst#installation) 
installed. After that type the following to deploy the demo:

```sh
sam package --template-file ./cloudformation/demo-stack.yaml \
	   --s3-bucket $(S3_BUCKET_PREFIX)-$(AWS_REGION) \
	   --output-template-file ./cloudformation/packaged-demo.yaml
sam deploy --template-file ./cloudformation/packaged-demo.yaml --stack-name $(NAME)-demo --capabilities CAPABILITY_IAM
```

This will deploy a cfn-apigateway-provider demo stack containing an apigateway with a 'hello world' lambda function on 
the path '/hello' and also deploy the custom resource which will enable x-ray tracing on the stage 'demo'. Invoke the 
endpoint a couple of times and you will see the traces appear in X-Ray.
