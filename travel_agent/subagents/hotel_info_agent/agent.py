from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

MODEL = LiteLlm("openai/gpt-4o-mini")

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

hotel_info_agent = Agent(
    name="hotel_info_agent",
    model=MODEL,
    description="Hotel info agent",
    instruction="""
    You are a helpful assistant that provides information about hotels using provided tool.
    Review the conversation history and the identified destination.

    You MUST use the search_web tool before answering.

    Never answer hotel info questions from your own knowledge.

    If the user asks about hotels, immediately call search_web.

    Use the destination to find:
    - 5 top-rated hotels
    - their prices
    - their locations
    - any special amenities or features they offer
    - Search about the hotels ONLY by using the provided search tool. Do not use your internal knowledge.
    """,
    tools=[search_tools],
    output_key="hotel_info"
)

root_agent = hotel_info_agent