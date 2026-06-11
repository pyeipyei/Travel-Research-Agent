from google.adk.agents import SequentialAgent, ParallelAgent, Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool
from dotenv import load_dotenv

# from .subagents.router_agent.agent import router_agent

from .subagents.attraction_info_agent.agent import attraction_info_agent
from .subagents.weather_info_agent.agent import weather_info_agent
from .subagents.hotel_info_agent.agent import hotel_info_agent
# from .subagents.summarizer_agent.agent import summarizer_agent

load_dotenv()

MODEL = LiteLlm("openai/gpt-4o-mini")

################################################
from langfuse import get_client

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

from openinference.instrumentation.google_adk import GoogleADKInstrumentor

GoogleADKInstrumentor().instrument()

##################################################
root_agent = Agent(
    name="travel_agent",
    model=MODEL,
    instruction="""
    You are an expert travel coordinator. 
    1. Your main job is to plan a trip based on the user's request by parallely calling the necessary sub-agents to gather information.
    2. Analyze the user's prompt to understand exactly what information they need.
    3. If the user asks to plan a trip, you should call all the tools parallely to gather comprehensive information about attractions, weather, and hotels.
    4. If user asks for specific information, call ONLY the tools (sub-agents) necessary to satisfy the request. Do not call irrelevant tools.
    5. Once you receive the tool outputs, synthesize and summarize them into a polished, cohesive travel guide response for the user.
    """,
     tools=[
        AgentTool(agent=attraction_info_agent),
        AgentTool(agent=weather_info_agent),
        AgentTool(agent=hotel_info_agent),
    ],
)

# coordinator_agent = Agent(
#     name="travel_coordinator",
#     model=MODEL,
#     instruction="Dynamically call the necessary tools to gather travel info and pass the raw details forward.",
#     tools=[
#         AgentTool(agent=attraction_info_agent),
#         AgentTool(agent=weather_info_agent),
#         AgentTool(agent=hotel_info_agent),
#     ],
# )

# # 2. Sequential pipeline to ensure the summarizer always runs last
# root_agent = SequentialAgent(
#     name="travel_agent_pipeline",
#     sub_agents=[
#         coordinator_agent,
#         summarizer_agent
#     ]
# )