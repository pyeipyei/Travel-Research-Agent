from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
# from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset 
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StdioServerParameters, 
)

from pathlib import Path
import sys

server_path = (
    Path(__file__).resolve().parent.parent.parent
    / "mcp_server"
    / "web_search_server.py"
)

search_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[str(server_path)]
        )
    )
)

MODEL = LiteLlm("openai/gpt-4o-mini")

weather_info_agent = Agent(
    name="weather_info_agent",
    model=MODEL,
    description="Weather info agent",
    instruction="""
    You are a helpful assistant that provides information about weather using provided tool. 
    Review the conversation history and the identified destination.

    You MUST use the search_web tool before answering.

    Never answer weather questions from your own knowledge.

    If the user asks about weather, immediately call search_web.

    Use the destination to find:
    - current weather conditions at there
    - weather forecast for the next 5 days
    - Search about the weather conditions ONLY by using the provided ***search tool***. Do not use your internal knowledge.
    """,
    output_key="weather_info",
    tools = [search_tools]
)

root_agent = weather_info_agent
