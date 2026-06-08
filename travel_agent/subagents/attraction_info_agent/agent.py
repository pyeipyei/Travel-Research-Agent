from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
# from google.adk.tools import google_search

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset 
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StdioServerParameters, 
)

search_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=["mcp_server/web_search_server.py"]
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
    Your task is to recommend attractions and activities.

    Review the conversation history and the identified destination.

    Use the destination to find:
    - tourist attractions
    - local food experiences
    - shopping areas
    - entertainment options

    Rules:
    - Use only the provided destination.
    - Do not search for hotels.
    - Do not provide weather information.
    """,

    tools=[search_tools],
    output_key="attraction_info",
)