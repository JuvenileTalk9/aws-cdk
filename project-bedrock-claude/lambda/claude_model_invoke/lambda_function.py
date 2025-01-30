import json

import boto3
import botocore


def lambda_handler(event, context):

    # パラメータ
    region_name = "us-east-1"
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    accept = "application/json"
    contentType = "application/json"
    outputText = "\n"

    # モデルに入力するプロンプト
    prompt = event["prompt"]

    # モデルが要求するフォーマットに形成
    # Claude 3 Sonnet の場合のフォーマットは以下URLに記載
    # https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/model-catalog/serverless/anthropic.claude-3-sonnet-20240229-v1:0
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 8192,
            "temperature": 0,
            "top_p": 0.9,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }
    )

    try:
        # クライアントを作成
        bedrock_client = boto3.client("bedrock-runtime", region_name=region_name)
        # 推論実行
        response = bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
    except botocore.exceptions.ClientError as e:
        # 必要に応じてエラーハンドリング
        return {"statusCode": 500, "body": json.dumps(f"Internal Server Error\n{e}")}

    # 出力をパースして表示
    response_body = json.loads(response.get("body").read())
    outputText = response_body["content"][0]["text"]

    return {"statusCode": 200, "body": outputText}
