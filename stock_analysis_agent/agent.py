from google.adk.agents.llm_agent import Agent,LlmAgent
from google.adk.agents import ParallelAgent
from google.genai import types

from google.adk.agents import SequentialAgent
# from google.adk.tools import google_search
from tools.customtool import get_stock_data, get_stock_metrics, get_stock_chart,ta_bmc,ta_bac,va_bmc
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
    # tools=[get_stock_metrics],
    **FUNDAMENTAL_AGENT_CONFIG
)

# Summary and Recommendation Agent
summary_agent = Agent(
    model='gemini-3-flash-preview', #'gemini-3-flash-preview'
    **SUMMARY_AGENT_CONFIG
)

# Visualization Agent 
visualization_agent = Agent(
    model='gemini-3-pro-image-preview', #'gemini-2.5-flash-image', #'gemini-3-pro-image-preview'
    # generate_content_config= types.GenerateContentConfig(temperature=0.2),
    before_model_callback=va_bmc,
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

root_agent = stock_research_workflow
# root_agent = visualization_agent 