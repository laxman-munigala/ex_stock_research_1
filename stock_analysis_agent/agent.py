from google.adk.agents.llm_agent import Agent,LlmAgent
from google.adk.agents import ParallelAgent
from google.adk.agents import SequentialAgent
from google.adk.tools import google_search
from tools.customtool import get_stock_data, get_stock_metrics, get_stock_chart,ta_bmc,ta_bac
import os
from google.adk.models.lite_llm import LiteLlm  # For multi-model support
from .prompts import (
    TECHNICAL_AGENT_CONFIG,
    FUNDAMENTAL_AGENT_CONFIG,
    SUMMARY_AGENT_CONFIG,
    VISUALIZATION_AGENT_CONFIG
)

technical_agent = Agent(
    model='gemini-3-flash-preview',
    tools=[get_stock_chart],
    before_model_callback=ta_bmc,
    before_agent_callback=ta_bac,
    **TECHNICAL_AGENT_CONFIG
)

# Fundamental Analysis Agent
fundamental_agent = Agent(
    model=LiteLlm(model="perplexity/sonar-pro",stream=True,
    web_search_options={
        "search_type": "pro"
    }),
    **FUNDAMENTAL_AGENT_CONFIG
)

# Summary and Recommendation Agent
summary_agent = Agent(
    model='gemini-2.5-flash-lite', #'gemini-3-flash-preview'
    **SUMMARY_AGENT_CONFIG
)

# Visualization Agent
visualization_agent = Agent(
    model='gemini-2.5-flash-image', #'gemini-3-pro-image-preview'
    **VISUALIZATION_AGENT_CONFIG
)

# Define the workflow using Parallel and Sequential agents
# 1. Run Technical and Fundamental analysis in parallel
analysis_parallel_agent = ParallelAgent(
    sub_agents=[technical_agent,fundamental_agent],
    name='analysis_parallel_agent',
    description='Runs technical and fundamental analysis in parallel.'
)

# 2. Sequential workflow: Analysis -> Summary -> Visualization
stock_research_workflow = SequentialAgent(
    sub_agents=[analysis_parallel_agent, summary_agent,visualization_agent],
    name='stock_research_workflow',
    description='Sequential workflow for stock research: Analysis, Summary, and Visualization.'
)

async def run_analysis(ticker: str):
    """
    Orchestrates the multi-agent workflow using the new ADK API.
    """
    print(f"Starting analysis for {ticker}...")

    # Run the entire workflow
    # The input to the first agent (ParallelAgent) will be the ticker
    result = await stock_research_workflow.run(f"Perform comprehensive analysis for {ticker}")
    
    # The result of a SequentialAgent is the result of the last agent in the sequence
    # The state will contain all the output_keys
    
    print(f"Analysis for {ticker} complete.")

    # Accessing the state from the result if possible, or returning the final content
    # In ADK, the result object usually contains the final response and the state
    return {
        "technical_report": result.state.get('technical_report'),
        "fundamental_report": result.state.get('fundamental_report'),
        "summary_report": result.state.get('summary_report'),
        "visualization_report": result.state.get('visualization_report')
    }

# Root Agent for ADK orchestration (if needed by main.py)
# root_agent = stock_research_workflow
# root_agent = fundamental_agent 
root_agent = stock_research_workflow