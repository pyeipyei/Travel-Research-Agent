from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

session_service = InMemorySessionService()

runner = Runner(
    app_name="travel_app",
    agent=root_agent,
    session_service=session_service
)

async def run_agent(user_message):

    session = await session_service.create_session(
        app_name="travel_app",
        user_id="streamlit_user"
    )

    response_text = ""
    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    ):
        if event.is_final_response():
            response_text = event.content.parts[0].text

    return response_text