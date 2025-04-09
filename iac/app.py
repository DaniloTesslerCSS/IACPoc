import json
import aws_cdk as cdk

from stacks.ecscluster import ECSCluster
from stacks.vpc import VPC
from stacks.ecr import ECR
from stacks.ecstaskdefinition import ECSTaskDefinition
from stacks.ecsservice import ECSService
from stacks.loadbalancer import LoadBalancer

# ****** INITIATE CDK  ******
app = cdk.App()

env = app.node.try_get_context("env")

if env == "" or env is None :
     raise Exception("No environment provided")

# ****** CONFIG ****** 
# Prepare the configuration files, merging the common and the env specific
with open("../configs/common.json") as f:
    configCommon = json.load(f)

with open("../configs/" + env + ".json") as f:
    configEnv = json.load(f)

config = configCommon | configEnv

# ****** NAMING CONVENTION  ******
stackNamePattern = config["ProjectName"] + config["EnvironmentType"]

if "EnvironmentName" in config: 
    stackNamePattern = stackNamePattern + config["EnvironmentName"]

config["StackNamePattern"] = stackNamePattern


# ****** PERPARE CDK CONFIGURATION  ******
cdkEnv = cdk.Environment(account = config["Account"], region = config["Region"])

# ****** STACK EXECUTION  ******
vpc = VPC(app, stackNamePattern + "vpc", config = config, env = cdkEnv)
ecsCluster = ECSCluster(app, stackNamePattern + "ecsCluster", vpc = vpc, config = config, env = cdkEnv)
ecr = ECR(app, stackNamePattern + "ecrRepo", config = config, env = cdkEnv)
ecsTaskDefinition = ECSTaskDefinition(app, stackNamePattern + "ecsTaskDefenition", ecr = ecr, envName = env, config = config, env = cdkEnv)
ecsService = ECSService(app, stackNamePattern + "ecsService", cluster = ecsCluster, taskDefinition = ecsTaskDefinition, vpc = vpc, config = config, env = cdkEnv)
loadBalancer = LoadBalancer(app, stackNamePattern + "lb", vpc = vpc, ecsService = ecsService, config = config, env = cdkEnv)

# ****** CDK STACK EXECUTION  ******
app.synth()