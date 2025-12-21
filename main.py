import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types
from stock_analysis_agent.agent import root_agent
import logging,random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

async def main():
    # Use InMemoryRunner which uses in-memory session and artifact services
    # Using async context manager for automatic cleanup (calls runner.close())
    async with InMemoryRunner(agent=root_agent) as runner:
        user_id = f"user_123_{random.random()}_{random.random()}"
        session_id = f"session_456_{random.random()}_{random.random()}"


        initial_state = {
            "technical_report": None,
            "fundamental_report": None,
            "ticker": "AAPL"
        }


        # Create a session
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )
        
        print(f"Starting session {session_id} for user {user_id}...")
        
        # Call the agent
        new_message = types.Content(parts=[types.Part(text="Start the analysis")])
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"---- ---- Agent: {event.author} :: {part.text}")

        # Cleanup the session explicitly before exiting the context
        print(f"Cleaning up session {session_id}...")
        await runner.session_service.delete_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )

if __name__ == "__main__":
    asyncio.run(main())
