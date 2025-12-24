import asyncio, datetime
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

        ticker = "NBIS"
        initial_state = {
            "technical_report": None,
            "fundamental_report": None,
            "ticker": ticker
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
        
        outputs = {
            "technical_analysis_agent":[],
            "fundamental_analysis_agent":[],
            "summary_recommendation_agent":[],
            "visualization_agent":[]
        }

        # with open(f"outputs/{ticker}_output.md", "a") as f:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        # f.write(f"# {event.author}\n\n")
                        # f.write(f"{part.text}\n\n")
                        outputs[event.author].append(part.text)
                    if part.inline_data and part.inline_data.mime_type == 'image/png':
                        # f.write(f"# {event.author}\n\n")
                        part.as_image().save(f"outputs/{ticker}_output.png")

        # Cleanup the session explicitly before exiting the context
        print(f"Cleaning up session {session_id}...")
        await runner.session_service.delete_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        with open(f"outputs/{ticker}_output.md", "w") as f:
            f.write(f"# Analysis of {ticker} done at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')}")
            f.write(f"# Stock chart of {ticker} used for Technical Analysis\n\n")
            f.write(f"![{ticker} chart](./{ticker}_chart.png)")

            for key in outputs.keys():
                f.write(f"\n\n# {key}\n\n")
                for item in outputs[key]: 
                    f.write(f"{item}\n\n")
            f.write(f"![{ticker} Recomendation](./{ticker}_output.png)")

if __name__ == "__main__":
    asyncio.run(main())
