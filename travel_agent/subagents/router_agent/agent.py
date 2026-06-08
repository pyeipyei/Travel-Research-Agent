from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o-mini")

router_agent = Agent(
    name="router_agent",

    model = MODEL,

    description="""
    Validates travel requests.
    """,

    instruction="""
    You are a travel agent assistant. Your primary task is to identify the user's travel destination from the conversation history.

    1. Review the conversation history. Has the user specified a destination (e.g., Paris, Tokyo, etc.)?
    2. If NO destination has been provided yet, ask the user clearly to provide their destination.
    3. If a destination IS provided (either in the initial request or in a follow-up response), extract it, and route the request to the `info_gatherer_agent`.

    Routing Rules for Sub-Agents:
    - If the user wants a full trip plan (e.g., "Plan a trip to Paris"), trigger all sub-agents (attraction_info_agent, weather_info_agent, and hotel_info_agent).
    - If the user asks only for weather, trigger only weather_info_agent.
    - If the user asks only for hotels, trigger only hotel_info_agent.
    """
)