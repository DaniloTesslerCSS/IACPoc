from constructs import Construct
from aws_cdk import (
    aws_ecs as ecs,
    Stack
)

class ECSCluster(Stack):
    
    def __init__(self, scope: Construct, id: str, vpc, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(self, id,
                            vpc = vpc.vpc,
                            cluster_name = id)