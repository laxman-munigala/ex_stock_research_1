# Context

## Current Focus
Implementation of the Multi-Agent System. The core tools for data fetching and chart generation are implemented in `tools/customtool.py`. The focus is now on defining the specific agents (Technical, Fundamental, Summary, Visualization) and orchestrating them in `main.py`.

## Recent Changes
- **Agent Refinement**: Updated the agent structure to include Technical Analysis, Fundamental Analysis, Summary and Recommendation, and Visualization agents.
- **Dependencies**: Added `google-adk`, `litellm`, `mplfinance`, and `yfinance` to `pyproject.toml`.
- **Tools**: Enhanced `tools/customtool.py` with `get_stock_data`, `generate_stock_chart` (using `mplfinance`), and `get_stock_metrics`.
- **Agents**: Created a prototype agent in `test_agent_one/agent.py` using `google-adk` and `google_search` tool.
- **Memory Bank**: Updated `context.md` to reflect current project state.

## Next Steps
1.  **Agent Definition**: Create the specific agent definitions (Technical, Fundamental, Summary, Visualization) utilizing the tools in `tools/customtool.py`.
2.  **Orchestration**: Implement the workflow in `main.py` to coordinate the agents using Google ADK.
3.  **CLI Integration**: Ensure `main.py` accepts user input and drives the process.
4.  **Testing**: Verify the end-to-end flow with a real ticker.
