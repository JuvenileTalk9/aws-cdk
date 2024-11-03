from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
)
from constructs import Construct

from .network_stack import NetworkStack


class EC2Stack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, network: NetworkStack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key_pair = ec2.KeyPair(
            self,
            id="key_pair",
            key_pair_name="ec2_key_pair",
            type=ec2.KeyPairType.RSA,
        )
        key_pair.apply_removal_policy(RemovalPolicy.DESTROY)

        public_ec2_1 = ec2.Instance(
            self,
            id="public_ec2_1",
            instance_name="public_ec2_1",
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2,
                ec2.InstanceSize.MICRO,
            ),
            key_pair=key_pair,
            vpc=network.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=network.security_group_for_public_instance,
        )
        public_ec2_1.apply_removal_policy(RemovalPolicy.DESTROY)

        private_ec2_1 = ec2.Instance(
            self,
            id="private_ec2_1",
            instance_name="private_ec2_1",
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2,
                ec2.InstanceSize.MICRO,
            ),
            key_pair=key_pair,
            vpc=network.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            security_group=network.security_group_for_private_instance,
        )
        private_ec2_1.apply_removal_policy(RemovalPolicy.DESTROY)
