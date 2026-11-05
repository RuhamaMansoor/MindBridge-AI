
import boto3
from botocore.exceptions import BotoCoreError, ClientError

REGION = "eu-north-1"
MODEL_ID = "eu.amazon.nova-lite-v1:0"

client = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)

try:
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "Say hello and introduce yourself in one sentence."
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 100,
            "temperature": 0.2
        }
    )

    for block in response["output"]["message"]["content"]:
        if "text" in block:
            print("AI Response:", block["text"])

except (ClientError, BotoCoreError) as error:
    print("Bedrock Error:", error)
