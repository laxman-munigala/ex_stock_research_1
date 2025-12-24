from google.adk.agents.llm_agent import Agent,LlmAgent
from google.adk.agents import ParallelAgent
from google.adk.agents import SequentialAgent
from google.adk.tools import google_search
from tools.customtool import get_stock_data, get_stock_metrics, get_stock_chart,ta_bmc,ta_bac
import os
from google.adk.models.lite_llm import LiteLlm  # For multi-model support

technical_agent = Agent(
    model='gemini-3-flash-preview',
    tools=[get_stock_chart], 
    name='technical_analysis_agent',
    description='You are a technical financial analyst expert.',
    instruction="""
        You are a technical financial analyst expert. Look at the provided stock chart of {ticker} and then provide the technical analysis. DO not make up, provided analysis based on attached chart only.
    """,
    before_model_callback=ta_bmc,
    before_agent_callback=ta_bac,
    output_key='technical_report'
)

# Fundamental Analysis Agent
fundamental_agent = Agent(
    model=LiteLlm(model="perplexity/sonar-pro",stream=True,
    web_search_options={
        "search_type": "pro"
    }),
    name='fundamental_analysis_agent',
    description='You are a financial research assistant.',
    instruction="""
You will be performing a concise fundamental analysis of a stock, focusing on qualitative information and context rather than raw quantitative metrics. The user has already obtained basic financial metrics from other sources and needs you to provide analyst estimates, sector analysis, growth prospects, and other qualitative insights.

Here is the stock to analyze:
<stock_symbol>
{ticker}
</stock_symbol>

The user already has quantitative metrics (P/E ratio, P/S ratio, Debt/Equity, revenue, net income, margins, ROE, etc.) from other sources. Your task is to provide:

1. **Key Valuation Metrics Context**: Brief qualitative assessment of whether current valuation ratios (P/E, P/S, Debt/Equity) are high, low, or fair relative to historical averages and industry peers
2. **Recent Financial Performance Context**: Qualitative interpretation of the revenue and net income trends over the last 3 years and TTM - are they accelerating, decelerating, stable? What's driving these trends?
3. **Profitability Context**: Brief assessment of margin trends and ROE - are they improving, declining, or stable? How do they compare to competitors?
4. **Analyst Outlook**: Summary of analyst consensus for the next 12 months including price targets, ratings (buy/hold/sell distribution), and key factors analysts are watching
5. **Sector Analysis**: Brief overview of the sector's current conditions, competitive positioning of this company within the sector, and major industry trends affecting the company
6. **Growth Prospects and Future Outlook**: Forward-looking qualitative assessment covering growth drivers, risks, strategic initiatives, and long-term prospects

Before providing your final analysis, use a <scratchpad> to organize your thoughts about each category and identify the most important qualitative insights to include.

Your output should be:
- Easy to digest and concise
- Organized with clear section headers for each of the 6 categories above
- Use very short bullet points (one line each when possible)
- Focus on qualitative insights, context, and interpretation rather than listing raw numbers
- Avoid jargon where possible; when technical terms are necessary, keep explanations brief
- Limit the entire analysis to what can be read in 2-3 minutes

Format your final response inside <analysis> tags with clear section headers and bullet points.
    """,
    output_key='fundamental_report'
)

# Summary and Recommendation Agent
summary_agent = Agent(
    model='gemini-2.5-flash-lite', #'gemini-3-flash-preview'
    name='summary_recommendation_agent',
    description='Synthesizes technical and fundamental analysis into a final recommendation.',
    instruction="""
    You are a Senior Investment Strategist.
    Your goal is to synthesize the reports from the Technical Analysis Agent and the Fundamental Analysis Agent.
    1. Review both reports carefully .

    <technical_report>
    {technical_report}
    </technical_report>

    <fundamental_report>
    {fundamental_report}
    </fundamental_report>

    2. Provide a final investment recommendation (Buy, Sell, or Hold).
    3. Include short-term and long-term predictions with clear reasoning.
    """,
    output_key='summary_report'
)

# Visualization Agent
visualization_agent = Agent(
    model='gemini-2.5-flash-image', #'gemini-3-pro-image-preview'
    name='visualization_agent',
    description='Generates visual reports and charts for the stock analysis.',
    instruction="""
    Your goal is to create a visual summary/image of the stock analysis.Do not show stock charts,bars.
    Use the below summary and recomendation and create an image to depict this. 
    <summary_report>
    {summary_report}
    </summary_report>

        Create a visual with key metrics which is visually appealing, highlight recomendation key points for short terma and long term

    """,
    output_key='visualization_report'
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