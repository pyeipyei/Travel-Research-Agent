from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
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

weather_info_agent = Agent(
    name="weather_info_agent",
    model=MODEL,
    description="Weather info agent",
    instruction="""
    You are a helpful assistant that provides information about weather. 
    Review the conversation history and the identified destination.

    Use the destination to find:
    - current weather conditions at there
    - weather forecast for the next 5 days
    """,
    output_key="weather_info",
    tools = [search_tools]
)
