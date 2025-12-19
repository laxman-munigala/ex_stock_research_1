import yfinance as yf
import pandas as pd
from typing import Literal
import mplfinance as mpf

def get_stock_data(
    ticker: str, 
    number_of_days: int, 
    timeframe_unit: Literal["day", "hour", "15min"]
) -> pd.DataFrame:
    """
    Retrieves historical stock data for a given ticker using yfinance.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        number_of_days: The number of days of historical data to retrieve.
        timeframe_unit: The interval of the data. Supported values are 'day', 'hour', and '15min'.

    Returns:
        A pandas DataFrame containing the historical stock data with columns:
        Open, High, Low, Close, Volume, etc.
    """
    # Map timeframe_unit to yfinance interval strings
    interval_map = {
        "day": "1d",
        "hour": "1h",
        "15min": "15m"
    }
    
    interval = interval_map.get(timeframe_unit, "1d")
    period = f"{number_of_days}d"
    
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    
    return df


def generate_stock_chart(df: pd.DataFrame, ticker: str, output_path: str) -> None:
    """
    Generates a candlestick chart for the given stock data using mplfinance and saves it to a file.

    This function creates a financial chart with candlesticks, volume, and moving averages
    for the provided stock data DataFrame. The chart is saved as an image file at the specified path.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing OHLC (Open, High, Low, Close) and Volume data,
                           typically returned from get_stock_data(). Must include columns: Open, High, Low, Close, Volume.
        ticker (str): The stock ticker symbol (e.g., 'AAPL') used for the chart title.
        output_path (str): File path where the chart image will be saved (e.g., 'output/chart.png').
                           Supported formats include PNG, JPG, PDF, etc.

    Returns:
        None: The function saves the chart to the specified file and does not return any value.

    Raises:
        ValueError: If the DataFrame does not contain the required OHLC columns.
        Exception: If there are issues with plotting or saving the file (e.g., invalid path).

    Example:
        df = get_stock_data('AAPL', 30, 'day')
        generate_stock_chart(df, 'AAPL', 'output/aapl_chart.png')
    """
    # Validate that the DataFrame has required columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain the following columns: {required_columns}")

    # Generate the candlestick chart with volume
    mpf.plot(df, type='candle', style='charles', volume=True, title=f'{ticker} Stock Chart', savefig=output_path)


def get_stock_metrics(ticker: str) -> str:
    """
    Retrieves and summarizes key financial metrics for a given stock ticker using yfinance.

    This function fetches earnings data for the last 4 quarters and last 2 years, along with
    key financial metrics from the stock's info. It then formats and returns a summary string.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        A formatted string containing summarized financial metrics including revenue, net profit,
        growth, P/E ratio, P/S ratio, market cap, debt, debt-to-equity ratio, and earnings data.
    """
    stock = yf.Ticker(ticker)

    # Get quarterly earnings for the last 4 quarters
    quarterly_earnings = stock.quarterly_earnings
    last_4_quarters = quarterly_earnings.tail(4) if quarterly_earnings is not None and not quarterly_earnings.empty else None

    # Get annual earnings for the last 2 years
    annual_earnings = stock.earnings
    last_2_years = annual_earnings.tail(2) if annual_earnings is not None and not annual_earnings.empty else None

    # Get key metrics from info
    info = stock.info
    market_cap = info.get('marketCap', 'N/A')
    pe_ratio = info.get('trailingPE', 'N/A')
    ps_ratio = info.get('priceToSalesTrailing12Months', 'N/A')
    total_debt = info.get('totalDebt', 'N/A')
    debt_to_equity = info.get('debtToEquity', 'N/A')

    # Extract revenue, net income, and growth from annual earnings
    if last_2_years is not None and len(last_2_years) > 0:
        revenue = last_2_years['Revenue'].iloc[-1] if 'Revenue' in last_2_years.columns else 'N/A'
        net_income = last_2_years['Net Income'].iloc[-1] if 'Net Income' in last_2_years.columns else 'N/A'
        # Calculate YoY revenue growth if possible
        if len(last_2_years) >= 2:
            rev_prev = last_2_years['Revenue'].iloc[-2]
            rev_curr = last_2_years['Revenue'].iloc[-1]
            growth = f"{((rev_curr - rev_prev) / rev_prev * 100):.2f}%" if rev_prev != 0 else 'N/A'
        else:
            growth = 'N/A'
    else:
        revenue = 'N/A'
        net_income = 'N/A'
        growth = 'N/A'

    # Format the summary string
    summary = f"""
Stock Metrics for {ticker.upper()}:

Market Cap: {market_cap}
P/E Ratio: {pe_ratio}
P/S Ratio: {ps_ratio}
Total Debt: {total_debt}
Debt to Equity: {debt_to_equity}
Latest Annual Revenue: {revenue}
Latest Annual Net Income: {net_income}
Revenue Growth (YoY): {growth}

Quarterly Earnings (Last 4 Quarters):
{last_4_quarters.to_string(index=True) if last_4_quarters is not None else 'N/A'}

Annual Earnings (Last 2 Years):
{last_2_years.to_string(index=True) if last_2_years is not None else 'N/A'}
"""

    return summary
