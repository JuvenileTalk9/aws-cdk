import aws_cdk as core
import aws_cdk.assertions as assertions

from project_s3.project_s3_stack import ProjectS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in project_s3/project_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectS3Stack(app, "project-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
