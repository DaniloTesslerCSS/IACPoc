from constructs import Construct
from aws_cdk import (
    aws_ecs as ecs,
    aws_iam as iam,
    Stack
)

class ECSTaskDefinition(Stack):
    
    def __init__(self, scope: Construct, id: str, ecr, envName, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.role = iam.Role(
            self, id + "ECSTaskExecutionRole",
            role_name = id + "ECSTaskExecutionRole",
            assumed_by = iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        policy_statement = iam.PolicyStatement(
            effect = iam.Effect.ALLOW,
            actions = [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "ssm:PutParameter",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:GetParametersByPath"
            ],
            resources=["*"]
        )
        
        self.role.add_to_policy(policy_statement)

        self.task = ecs.FargateTaskDefinition(
            self, id,
            task_role = self.role,
            execution_role = self.role,
            cpu = 1024,
            memory_limit_mib = 3072,
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=ecs.CpuArchitecture.X86_64,
                operating_system_family=ecs.OperatingSystemFamily.LINUX
            )            
        )

        container = self.task.add_container(
            id + "container",
            image = ecs.ContainerImage.from_ecr_repository(ecr.ecr),
            memory_limit_mib = 3072,
            cpu = 1024,
            logging = ecs.LogDriver.aws_logs(stream_prefix = id),
            environment = { "environment": envName }
        )

        container.add_port_mappings(
            ecs.PortMapping(
                container_port=80,
                host_port=80,
                protocol = ecs.Protocol.TCP,
                name = "http",
                app_protocol = ecs.AppProtocol.http
            )
        )