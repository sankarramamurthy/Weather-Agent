import boto3
import json

client = boto3.client('bedrock-agent', region_name='us-east-1')


AGENT_ID = 'UUOUGYTK0O'  # From previous step
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:368559787488:function:bedrock-weather-function'

    #OpenAPI schema defining the tool

openapi_schema = {
    "openapi": "3.0.0",
    "info": {
        "title": "Weather API",
        "version": "1.0.0",
        "description": "API for getting weather forecasts for US cities"
    },
    "paths": {
        "/weather": {
            "get": {
                "summary": "Get weather forecast",
                "description": "Get weather forecast for a US city. Use when user asks about weather, temperature, or conditions.",
                "operationId": "getWeather",
                "parameters": [
                    {
                        "name": "city",
                        "in": "query",
                        "description": "US city name (e.g. 'Seattle', 'New York')",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "mode",
                        "in": "query",
                        "description": "Forecast type: 'hourly' or 'daily'",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["hourly", "daily"],
                            "default": "hourly"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Weather forecast",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "weather_report": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

print("Creating action group...")

try:
    response = client.create_agent_action_group(
        agentId=AGENT_ID,
        agentVersion='DRAFT',
        actionGroupName='weather-tools',
        actionGroupExecutor={'lambda': LAMBDA_ARN},
        apiSchema={'payload': json.dumps(openapi_schema)},
        description='Tools for getting weather information',
        actionGroupState='ENABLED'
    )

    print("✅ Action group created!")
    print(f"Action Group ID: {response['agentActionGroup']['actionGroupId']}")

except Exception as e:
    print(f"❌ Error: {str(e)}")