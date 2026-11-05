
"""
MindBridge AI - Strands SDK Smoke Test

Verifies:
1. Strands Agent initialization
2. Real AWS Bedrock model invocation
3. Successful model response

This is a live API test, not a clinical safety test.
"""

import sys

from strands import Agent
from strands.models import BedrockModel


def main():
    print("Starting real Strands + AWS Bedrock test...")

    try:
        model = BedrockModel(
            model_id="eu.amazon.nova-lite-v1:0",
            region_name="eu-north-1",
            temperature=0,
            max_tokens=100,
        )

        agent = Agent(
            model=model,
            system_prompt=(
                "You are a software connectivity test assistant. "
                "Answer the user's simple question accurately "
                "and briefly. Do not discuss company names, "
                "products, or confidential information."
            ),
            tools=[],
        )

        result = agent(
            "What is 2 plus 2? Reply with only the number."
        )

        response = str(result).strip()

        print("\nSTRANDS RESPONSE:", response)

        if response != "4":
            print("FAILED: Unexpected response.")
            return 1

        print(
            "SUCCESS: Real Strands SDK + "
            "AWS Bedrock integration verified."
        )
        return 0

    except Exception as exc:
        print(
            "FAILED:",
            type(exc).__name__,
            str(exc),
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
