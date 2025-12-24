# Technologies

## Core Stack
- **Language**: Python 3.12+
- **AI Framework**: Google ADK (Agent Development Kit) `google-adk>=1.21.0`
- **LLM**: 
    - Google Gemini (`gemini-3-flash-preview`, `gemini-2.5-flash-lite`, `gemini-3-pro-image-preview`)
    - Perplexity (`perplexity/sonar-pro`) via `litellm`

## Data & Analysis Libraries
- **`yfinance`**: Stock market data retrieval.
- **`pandas`**: Data manipulation and analysis.
- **`mplfinance`**: Chart generation.
- **`ta`** (Technical Analysis Library) or custom implementation: For calculating indicators like RSI, SMA.

## External APIs & Tools
- **Perplexity API**: For up-to-date web search, news, and fundamental analysis (via `litellm`).
- **Google Gemini Image Model**: For generating the final visual report.

## Development Tools
- **`uv`**: Python package and project manager (implied by `uv.lock`).
- **VS Code**: IDE.
- **`litellm`**: For LLM abstraction (dependency).

## Constraints
- **Rate Limits**: API rate limits for `yfinance` and Perplexity.
- **Context Window**: Managing context size when passing data between agents.
