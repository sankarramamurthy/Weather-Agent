import boto3
import json
import sys

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

AGENT_ID = 'UUOUGYTK0O'
AGENT_ALIAS_ID = 'I4LEYPTZLO'

def chat(message):
    """Send a message to the agent and display the response."""

    print(f"\n{'='*70}")
    print(f"You: {message}")
    print(f"{'='*70}\n")

    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId='test-session',
        inputText=message,
        enableTrace=True
    )

    print("Agent: ", end='', flush=True)

    for event in response['completion']:
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                print(chunk['bytes'].decode('utf-8'), end='', flush=True)

        elif 'trace' in event:
            trace = event['trace']
            if 'trace' in trace:
                trace_data = trace['trace']
                if 'orchestrationTrace' in trace_data:
                    orch = trace_data['orchestrationTrace']

                    if 'invocationInput' in orch:
                        inv = orch['invocationInput']
                        if 'actionGroupInvocationInput' in inv:
                            action = inv['actionGroupInvocationInput']
                            params = {p['name']: p['value'] for p in action.get('parameters', [])}
                            print(f"\n[Calling tool with params: {params}]")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    # Interactive mode
    print("\n🌤️  Weather Agent - Type 'exit' to quit\n")

    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if query:
                chat(query)
        except KeyboardInterrupt:
            break

    print("\n👋 Goodbye!\n")