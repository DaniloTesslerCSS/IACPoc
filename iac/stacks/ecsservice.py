from constructs import Construct
from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    Stack,
    Duration
)

class ECSService(Stack):
    
    def __init__(self, scope: Construct, id: str, cluster, taskDefinition, vpc, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        securityGroup = ec2.SecurityGroup(self, id + "sc",
            vpc = vpc.vpc,
            allow_all_outbound=True
        )

        securityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.all_traffic()
        )

        self.service = ecs.FargateService(self, id,
            cluster = cluster.cluster,
            task_definition = taskDefinition.task,
            desired_count = 0,
            assign_public_ip = True,
            service_name = id,
            health_check_grace_period = Duration.seconds(0),
            security_groups = [ securityGroup ]
        )  