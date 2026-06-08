from google.adk.agents import SequentialAgent, ParallelAgent
from dotenv import load_dotenv

from .subagents.router_agent.agent import router_agent

from .subagents.attraction_info_agent.agent import attraction_info_agent
from .subagents.weather_info_agent.agent import weather_info_agent
from .subagents.hotel_info_agent.agent import hotel_info_agent
from .subagents.summarizer_agent.agent import summarizer_agent

load_dotenv()

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

info_gatherer_agent = ParallelAgent(
    name="info_gatherer_agent",
    sub_agents=[
        attraction_info_agent,
        weather_info_agent,
        hotel_info_agent
    ]
)

root_agent = SequentialAgent(
    name="travel_agent",
    sub_agents=[
        router_agent,
        info_gatherer_agent,
        summarizer_agent
    ]
)