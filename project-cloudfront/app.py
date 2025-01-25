#!/usr/bin/env python3
import os

import aws_cdk as cdk

from project_cloudfront.project_cloudfront_stack import ProjectCloudfrontStack


app = cdk.App()

ProjectCloudfrontStack(
    app,
    "ProjectCloudfrontStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
