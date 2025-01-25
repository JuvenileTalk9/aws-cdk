import aws_cdk as core
import aws_cdk.assertions as assertions

from project_cloudfront.project_cloudfront_stack import ProjectCloudfrontStack

# example tests. To run these tests, uncomment this file along with the example
# resource in project_cloudfront/project_cloudfront_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectCloudfrontStack(app, "project-cloudfront")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
