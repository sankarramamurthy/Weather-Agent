import boto3
import json
import time

client = boto3.client('bedrock-agent', region_name='us-east-1')

ROLE_ARN = 'arn:aws:iam::368559787488:role/BedrockAgentRole'

print("Creating Bedrock agent...")

try:
    response = client.create_agent(
        agentName='weather-assistant',
        agentResourceRoleArn=ROLE_ARN,
        foundationModel='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        instruction=(
            "You are a helpful weather assistant. "
            "When users ask about weather in any US city, use the getWeather tool "
            "to fetch current conditions and forecasts. "
            "Provide friendly, conversational responses with relevant weather details. "
            "If asked about multiple cities, check each one. "
            "Always mention temperature, conditions, and any important weather alerts."
        ),
        idleSessionTTLInSeconds=600
    )

    agent_id = response['agent']['agentId']

    print(f"✅ Agent created successfully!")
    print(f"Agent ID: {agent_id}")
    print(f"Agent Name: {response['agent']['agentName']}")
    print(f"\nSave this Agent ID for the next steps!")

    # Save to file
    with open('agent-config.json', 'w') as f:
        json.dump({'agent_id': agent_id}, f)

except Exception as e:
    print(f"❌ Error: {str(e)}")