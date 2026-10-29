"""Amazon Bedrock AgentCore Runtime entrypoint."""
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from medguide.agent import build_agent

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload, context):
    prompt = payload.get("prompt")
    if not prompt:
        raise ValueError("Missing required field: prompt")
    agent = build_agent(audit_path=None)
    return str(agent(prompt)).strip()


if __name__ == "__main__":
    app.run()
