from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
# from google.adk.tools import google_search

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

attraction_info_agent = Agent(
    name="attraction_info_agent",
    model=MODEL,

    description="""
    Finds attractions, activities, and travel experiences for the destination.
    """,

    instruction="""
    Your task is to recommend attractions and activities using provided tool.

    Review the conversation history and the identified destination.

    You MUST use the search_web tool before answering.

    Never answer attractions, activities, and travel experiences questions from your own knowledge.

    If the user asks about attractions, activities, and travel experiences, immediately call search_web.

    Use the destination to find:
    - tourist attractions
    - local food experiences
    - shopping areas
    - entertainment options

    Rules:
    - Search about the destination ONLY by using the provided search tool. Do not use your internal knowledge.
    - Use only the provided destination.
    - Do not search for hotels.
    - Do not provide weather information.
    """,

    tools=[search_tools],
    output_key="attraction_info",
)

root_agent = attraction_info_agent