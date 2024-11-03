from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
)
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            id="Vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet-01",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="private-subnet-01",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )
        vpc.apply_removal_policy(RemovalPolicy.DESTROY)

        security_group_for_public_instance = ec2.SecurityGroup(
            self,
            id="security_group_for_public_instance",
            security_group_name="security_group_for_public_instance",
            vpc=vpc,
            allow_all_outbound=True,
        )
        security_group_for_public_instance.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="allow ssh access from any IPV4",
        )
        security_group_for_public_instance.apply_removal_policy(RemovalPolicy.DESTROY)

        security_group_for_private_instance = ec2.SecurityGroup(
            self,
            id="security_group_for_private_instance",
            security_group_name="security_group_for_private_instance",
            vpc=vpc,
            allow_all_outbound=True,
        )
        security_group_for_private_instance.add_ingress_rule(
            peer=ec2.Peer.ipv4("10.0.0.0/16"),
            connection=ec2.Port.tcp(22),
            description="allow ssh access from any IPV4",
        )
        security_group_for_private_instance.apply_removal_policy(RemovalPolicy.DESTROY)

        self.vpc = vpc
        self.security_group_for_public_instance = security_group_for_public_instance
        self.security_group_for_private_instance = security_group_for_private_instance
