import streamlit as st
import os
from dotenv import load_dotenv

from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

load_dotenv()  # Load environment variables

# Set API keys from environment
# os.environ["GROQ_API_KEY"]
# os.environ["LANGSMITH_API_KEY"]


def init_agent():
    # Setup credentials and API resource for Gmail
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)
    tools = toolkit.get_tools()
    
    # Initialize your chat model
    llm = init_chat_model("llama3-8b-8192", model_provider="groq")
    agent_executor = create_react_agent(llm, tools)
    return agent_executor

# Initialize the agent (cached)
agent_executor = init_agent()

st.title("AI Email Agent")

# Create a form for user input
with st.form("email_form"):
    user_prompt = st.text_input("Enter your command", placeholder="Send an email to user@gmail.com saying hello")
    submit_button = st.form_submit_button("Submit")

if submit_button and user_prompt:
    st.write("Processing your request...")
    # Create a placeholder for streaming output
    placeholder = st.empty()
    
    # Call the agent with streaming
    events = agent_executor.stream(
        {"messages": [("user", user_prompt)]},
        stream_mode="values",
    )
    # Update the placeholder with each streamed message
    for event in events:
        last_message = event["messages"][-1]
        placeholder.write(last_message.content)
