# Architecture

## System Overview
The application uses a multi-agent architecture built on the **Google Agent Development Kit (ADK)**. It follows a pipeline approach where data is collected, analyzed by specialized agents, and then synthesized into a final report.

## Components

### 1. Orchestration / Entry Point
- **`main.py`**: Handles user input (CLI) and initializes the agent workflow.
- **Root Agent**: Coordinates the sub-agents or manages the flow of information.

### 2. Agents
- **Data Collection Agent**:
    - **Responsibility**: Fetch raw data and prepare visualizations.
    - **Tools**: `yfinance` (market data), `matplotlib` (charting).
    - **Output**: Raw data (JSON/DataFrame) and Chart Image.
- **Technical Analysis Agent**:
    - **Responsibility**: Analyze price action and indicators.
    - **Input**: Historical price data, calculated indicators (SMA, RSI).
    - **Output**: Technical signals (Bullish/Bearish) and trend analysis.
- **Fundamental Analysis Agent**:
    - **Responsibility**: Analyze company health and market sentiment.
    - **Tools**: Google Search (News), Earnings APIs.
    - **Output**: Fundamental health score, news summary, earnings insights.
- **Summary & Recommendation Agent**:
    - **Responsibility**: Synthesize all information into a final verdict.
    - **Input**: Outputs from all other agents.
    - **Output**: Final text summary and generation of the visual report (using Gemini Image model).

## Data Flow
1.  User inputs Ticker.
2.  **Data Agent** fetches history -> calculates indicators -> draws chart.
3.  **Technical Agent** reads data/indicators -> generates technical report.
4.  **Fundamental Agent** searches news/earnings -> generates fundamental report.
5.  **Summary Agent** combines Chart + Technical Report + Fundamental Report -> Generates Final Visual Output.

## Directory Structure
- `main.py`: Entry point.
- `agents/`: Directory for agent definitions (to be created).
- `tools/`: Custom tools for agents (to be created).
- `output/`: Directory for generated reports.
