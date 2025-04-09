from constructs import Construct
from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    Stack
)

class LoadBalancer(Stack):
    
    def __init__(self, scope: Construct, id: str, vpc, ecsService, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        securityGroup = ec2.SecurityGroup(self, id + "sc",
            vpc = vpc.vpc,
            allow_all_outbound=True
        )

        securityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80)
        )

        self.loadBalancer = elbv2.ApplicationLoadBalancer(self, id,
            vpc = vpc.vpc,
            internet_facing = True,
            load_balancer_name = id
        )

        self.loadBalancer.add_security_group(securityGroup)

        self.targetGroup = elbv2.ApplicationTargetGroup(self, id + "tg",
            vpc = vpc.vpc,
            port = 80,
            protocol = elbv2.ApplicationProtocol.HTTP,
            target_type = elbv2.TargetType.IP
        )

        listener = self.loadBalancer.add_listener(id + "listener",
            port = 80,
            open = True
        )

        listener.add_targets(id + "ecstg",
            port = 80,
            targets=[ecsService.service]
        )        