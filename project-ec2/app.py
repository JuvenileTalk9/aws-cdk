#!/usr/bin/env python3
import os

import aws_cdk as cdk

from project_ec2.network_stack import NetworkStack
from project_ec2.ec2_stack import EC2Stack


app = cdk.App()

network = NetworkStack(
    app,
    "NetworkStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

EC2Stack(
    app,
    "EC2Stack",
    network,
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
