import aws_cdk as core
import aws_cdk.assertions as assertions

from project_ec2.project_ec2_stack import ProjectEc2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in project_ec2/project_ec2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectEc2Stack(app, "project-ec2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
