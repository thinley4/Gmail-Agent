from langchain_google_community import GmailToolkit

from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

os.environ["GROQ_API_KEY"]
# Set the API key
os.environ["LANGSMITH_API_KEY"]

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()
tools

llm = init_chat_model("llama3-8b-8192", model_provider="groq")


agent_executor = create_react_agent(llm, tools)

example_query = "Send an email to xyz@gmail.com saying hello"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()