# Architecture

## System Overview
The application uses a multi-agent architecture built on the **Google Agent Development Kit (ADK)**. It follows a pipeline approach where data is collected, analyzed by specialized agents, and then synthesized into a final report.

## Components

### 1. Orchestration / Entry Point
- **`main.py`**: Handles user input (CLI) and initializes the agent workflow.
- **Root Agent**: Coordinates the sub-agents or manages the flow of information.

### 2. Agents
- **Technical Analysis Agent**:
    - **Model**: `gemini-3-flash-preview`
    - **Responsibility**: Analyze price action and indicators.
    - **Input**: Historical price data, calculated indicators (SMA, RSI).
    - **Output**: Technical signals (Bullish/Bearish) and trend analysis.
- **Fundamental Analysis Agent**:
    - **Model**: `perplexity/sonar-pro` (via `litellm`)
    - **Responsibility**: Analyze company health and market sentiment.
    - **Tools**: Uses Perplexity's online search capabilities.
    - **Output**: Fundamental health score, news summary, earnings insights.
- **Summary & Recommendation Agent**:
    - **Model**: `gemini-2.5-flash-lite`
    - **Responsibility**: Synthesize all information into a final verdict.
    - **Input**: Outputs from Technical and Fundamental agents.
    - **Output**: Final text summary and recommendations.
- **Visualization Agent**:
    - **Model**: `gemini-3-pro-image-preview`
    - **Responsibility**: Generate the final visual report and charts.
    - **Input**: Summary, recommendations, and raw data.
    - **Output**: Final visual report (using Gemini Image model).

## Data Flow
1.  User inputs Ticker.
2.  **Parallel Execution**:
    - **Technical Agent** fetches data/indicators -> generates technical report.
    - **Fundamental Agent** searches news/earnings -> generates fundamental report.
3.  **Summary Agent** combines Technical Report + Fundamental Report -> Generates final verdict.
4.  **Visualization Agent** takes the summary output -> Generates Final Visual Output (Dashboard).
5.  **Output Generation**: System saves the visual report and creates a consolidated Markdown file.

## Directory Structure
- `main.py`: Entry point.
- `stock_analysis_agent/`: Directory for agent definitions and prompts.
- `tools/`: Custom tools for agents (data fetching, charting).
- `outputs/`: Directory for generated reports and artifacts.
