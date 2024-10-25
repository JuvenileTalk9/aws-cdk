from aws_cdk import (
    Duration,
    Stack,
    aws_s3,
    aws_kms,
)
from constructs import Construct


class ProjectS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_kms_key = aws_kms.Key(
            self,
            id="s3_kms_key",
            alias="s3_kms_key",
            key_spec=aws_kms.KeySpec.SYMMETRIC_DEFAULT,
            key_usage=aws_kms.KeyUsage.ENCRYPT_DECRYPT,
            enable_key_rotation=True,
            rotation_period=Duration.days(90),
            pending_window=Duration.days(7),
        )

        s3_bucket = aws_s3.Bucket(  # noqa
            self,
            id="s3_bucket",
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.KMS,
            encryption_key=s3_kms_key,
            bucket_key_enabled=True,
        )
