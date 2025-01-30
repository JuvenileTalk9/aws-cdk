import aws_cdk as core
import aws_cdk.assertions as assertions

from project_bedrock_claude.project_bedrock_claude_stack import ProjectBedrockClaudeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in project_bedrock_claude/project_bedrock_claude_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectBedrockClaudeStack(app, "project-bedrock-claude")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
