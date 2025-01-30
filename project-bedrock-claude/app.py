#!/usr/bin/env python3
import os

import aws_cdk as cdk

from project_bedrock_claude import (
    cloudfront,
    function,
    api_gateway,
)


app = cdk.App()

cloudfront.CloudFrontStack(
    app,
    "ProjectBedrockClaudeCloudFrontStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

function = function.FunctionStack(
    app,
    "ProjectBedrockClaudeFunctionStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

api_gateway.ApiGatewayStack(
    app,
    "ProjectBedrockClaudeApiGatewayStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
    claude_invoke_model_function=function.claude_invoke_model_function,
)

app.synth()
