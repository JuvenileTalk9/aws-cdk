from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct


class ApiGatewayStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        claude_invoke_model_function: lambda_.Function,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(
            self,
            id="invoke_model_api",
            rest_api_name="invoke_model_api",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
        )
        api.add_request_validator(
            id="request_validator",
            validate_request_body=True,
            validate_request_parameters=True,
        )

        api_key = api.add_api_key(
            id="invoke_model_api_key",
            api_key_name="invoke_model_api_key",
        )

        usage_plan = api.add_usage_plan(
            id="invoke_api_usage_plan",
            name="invoke_api_usage_plan",
            throttle=apigateway.ThrottleSettings(
                rate_limit=1,
                burst_limit=1,
            ),
            quota=apigateway.QuotaSettings(
                limit=50,
                period=apigateway.Period.DAY,
            ),
        )
        usage_plan.add_api_key(api_key)
        usage_plan.add_api_stage(
            api=api,
            stage=api.deployment_stage,
        )

        request_invoke_model = apigateway.Model(
            self,
            id="request_invoke",
            model_name="RequestInvokeModel",
            rest_api=api,
            content_type="application/json",
            schema=apigateway.JsonSchema(
                schema=apigateway.JsonSchemaVersion.DRAFT4,
                type=apigateway.JsonSchemaType.OBJECT,
                required=["prompt"],
                properties={
                    "prompt": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING
                    )
                },
            ),
        )

        invoke_model_api = api.root.add_resource("invoke")
        invoke_model_api.add_method(
            http_method="POST",
            api_key_required=True,
            request_parameters={
                "method.request.header.Content-Type": True,
                "method.request.header.x-api-key": True,
            },
            request_models={"application/json": request_invoke_model},
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_models={"application/json": apigateway.Model.EMPTY_MODEL},
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                )
            ],
            integration=apigateway.LambdaIntegration(
                claude_invoke_model_function,
                proxy=False,
                integration_responses=[
                    apigateway.IntegrationResponse(
                        status_code="200",
                        content_handling=apigateway.ContentHandling.CONVERT_TO_TEXT,
                        response_templates={
                            "application/json": "{\"message\": $input.json('$.body')}"
                        },
                        response_parameters={
                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                        },
                    ),
                ],
            ),
        )
