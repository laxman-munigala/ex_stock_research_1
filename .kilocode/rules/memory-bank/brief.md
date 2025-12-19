# Stock Research Application Project Brief

## Overview

Develop an AI-powered stock analysis application that accepts a stock ticker (e.g., AAPL, NVDA) as input and performs comprehensive fundamental and technical analysis to generate short-term and long-term predictions and recommendations. The application leverages a GenAI multi-agent solution to integrate price/volume data, technical indicators, earnings data, and relevant company information from search queries. The final output is a simple visual summary highlighting key points and recommendations, generated using a Google Gemini image model.

## Objectives

- Provide actionable insights for stock investment decisions.
- Demonstrate the effectiveness of multi-agent AI in financial analysis.
- Build a scalable foundation for incremental feature additions.

## Key Features

- **Input Handling**: Accept stock ticker symbols.
- **Data Integration**: Fetch historical price/volume data, calculate technical indicators, retrieve earnings reports, and search for company news.
- **Analysis Modules**:
  - Technical Analysis: Based on charts and indicators.
  - Fundamental Analysis: Based on earnings and news.
- **Output Generation**: Create a visual report with summary, key points, and recommendations.

## Architecture

The application is built on a Google ADK-based multi-agent framework, where specialized agents handle different aspects of the analysis:

- **Data Collection Agent**: Retrieves data from yfinance, computes indicators, and generates a stock chart image.
- **Technical Analysis Agent**: Analyzes the chart and indicators to derive technical insights and signals.
- **Fundamental Analysis Agent**: Processes earnings data and searches for company-related information to perform fundamental analysis.
- **Summary and Recommendation Agent**: Synthesizes inputs from other agents to formulate short-term and long-term predictions, then generates the final visual report using the Google Gemini image model.

Data flows from the Data Agent to the analysis agents, with the Summary Agent orchestrating the final output.

## Technologies

- **Programming Language**: Python
- **Data Source**: yfinance for stock data
- **Chart Generation**: Matplotlib or similar for initial charts
- **Search**: API for web search (e.g., Google Custom Search API)
- **AI Framework**: Google ADK for multi-agent orchestration
- **Image Generation**: Google Gemini image model
- **Other Libraries**: Pandas for data manipulation, Requests for API calls

## MVP Scope

Focus on core functionality for a quick build:

- Implement basic data fetching for the past year.
- Calculate essential indicators: Simple Moving Average (SMA), Relative Strength Index (RSI).
- Generate a simple line or candlestick chart.
- Fetch recent earnings data and basic news headlines.
- Set up multi-agent framework with placeholder logic for analysis.
- Integrate Google Gemini to create a basic visual summary (e.g., text overlay on chart with key points).

MVP deliverables: A command-line application that takes a ticker, processes data, and outputs a generated image file.

## Future Enhancements

- Add advanced indicators (e.g., MACD, Bollinger Bands).
- Integrate more data sources (e.g., SEC filings, social media sentiment).
- Enhance AI agents with more sophisticated models.
- Develop a web-based user interface.
- Implement backtesting for predictions.
- Add real-time data streaming.
- Expand to multi-stock portfolios.

This brief provides a foundation for building the MVP incrementally, allowing for rapid prototyping and iterative improvements.