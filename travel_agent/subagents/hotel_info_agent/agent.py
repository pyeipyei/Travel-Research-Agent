from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

MODEL = LiteLlm("openai/gpt-4o-mini")

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

hotel_info_agent = Agent(
    name="hotel_info_agent",
    model=MODEL,
    description="Hotel info agent",
    instruction="""
    You are a helpful assistant that provides information about hotels.
    Review the conversation history and the identified destination.

    Use the destination to find:
    - 5 top-rated hotels
    - their prices
    - their locations
    - any special amenities or features they offer
    """,
    tools=[search_tools],
    output_key="hotel_info"
)
