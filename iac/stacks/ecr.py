from constructs import Construct
from aws_cdk import (
    aws_ecr as ecr,
    Stack
)

class ECR(Stack):
    
    def __init__(self, scope: Construct, id: str, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.ecr = ecr.Repository(self, id, repository_name = id.lower())