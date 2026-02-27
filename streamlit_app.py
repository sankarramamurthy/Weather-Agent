import streamlit as st
import boto3
import requests
import json

BEDROCK_AGENT_ID = "UUOUGYTK0O"
BEDROCK_AGENT_ALIAS_ID = "I4LEYPTZLO"
AWS_REGION = "us-east-1"

# Function to interact with the AI Agent (Example using an API Gateway endpoint)
def invoke_agent_api(prompt):
    payload = {"prompt": prompt}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "Error: No response received")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to interact with the AI Agent (Example using Boto3 for Bedrock Agent Runtime)
def invoke_bedrock_agent(prompt):
    client = boto3.client('bedrock-agent-runtime', region_name=AWS_REGION)
    session_id = "demo_session" # Manage sessions for conversation history
    response = client.invoke_agent(
        agentId=BEDROCK_AGENT_ID,
        agentAliasId=BEDROCK_AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt
    )

    # Process the streaming response from Bedrock
    result = ''
    for event in response.get('completion'):
        chunk = event['chunk']
        result += chunk['bytes'].decode()
    return result

# --- Streamlit UI ---
st.set_page_config(page_title="AI Agent Interface")
st.title("Weather Forecast AI Agent")

prompt = st.text_area("Enter your prompt:", height=100)

if st.button("Ask AI"):
    with st.spinner("Agent thinking..."):
        # Choose the appropriate function based on your backend
        # response_text = invoke_agent_api(prompt) 
        response_text = invoke_bedrock_agent(prompt) #
        st.text_area("AI Response:", value=response_text, height=200)
