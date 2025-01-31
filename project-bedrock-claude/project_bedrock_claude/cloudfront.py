import os

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
)
from constructs import Construct


class CloudFrontStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket_name = "cloudfront-origin-bucket-juveniletalk9-dev"

        cloudfront_bucket = s3.Bucket(
            self,
            id="cloudfront_bucket",
            bucket_name=s3_bucket_name,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        s3_deployment.BucketDeployment(
            self,
            id="s3_deploy",
            sources=[
                s3_deployment.Source.asset(os.path.join("asset", "html")),
            ],
            destination_bucket=cloudfront_bucket,
        )

        cloudfront.Distribution(
            self,
            id="cloudfront_distribution",
            default_behavior=cloudfront.BehaviorOptions(
                # CloudFrontからのGetObjectを許可するバケットポリシーがS3に自動適用される
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    cloudfront_bucket
                )
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_200,
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=404,
                    response_page_path="/404-not-found.html",
                )
            ],
            default_root_object="index.html",
        )
