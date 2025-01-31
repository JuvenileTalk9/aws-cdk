import os

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct


class FunctionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam_role_for_lambda = iam.Role(
            self,
            id="iam_role_for_lambda",
            role_name="AWSLambdaReadOnlyRoleForAmazonBedrock",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        iam_role_for_lambda.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:Get*",
                    "bedrock:List*",
                ],
                resources=["*"],
            )
        )

        claude_invoke_model_function = lambda_.Function(
            self,
            id="claude_invoke_model_function",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset(
                os.path.join("asset", "lambda", "claude_model_invoke")
            ),
            timeout=Duration.minutes(1),
            role=iam_role_for_lambda,
        )

        self.claude_invoke_model_function = claude_invoke_model_function
