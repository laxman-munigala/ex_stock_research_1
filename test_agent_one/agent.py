from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    # model='gemini-2.5-flash',
    model='gemini-3-flash-preview',
    tools=[google_search],
    name='test_agent_one',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
