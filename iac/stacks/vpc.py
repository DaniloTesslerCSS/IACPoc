from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    Stack
)

class VPC(Stack):
    
    def __init__(self, scope: Construct, id: str, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id = config["VpcId"])