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

    # Calculate Moving Averages
    # df['SMA_21'] = df['Close'].rolling(window=21).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    # Calculate RSI (14 periods)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df = df.tail(250)
    # Create addplots
    apds = [
        # mpf.make_addplot(df['SMA_21'], color='blue', width=1.0),
        mpf.make_addplot(df['SMA_50'], color='orange', label='SMA_50',width=1.0),
        mpf.make_addplot(df['SMA_200'], color='red', label='SMA_200', width=1.0),
        mpf.make_addplot(df['RSI'], panel=2, color='purple', ylabel='RSI', width=1.0)
    ]

    # Generate the candlestick chart with volume and indicators
    fig, axes = mpf.plot(
        df,
        type='candle',
        style='charles',
        volume=True,
        addplot=apds,
        title=f'{ticker} Stock Chart',
        returnfig=True,
        figsize=(12,6),
        panel_ratios=(6, 2, 2)
    )
    
    # Add legends
    # axes[0] is the main chart primary axis
    axes[0].legend()
    
    # axes[4] is the RSI chart primary axis (Panel 2)
    # Structure is [Main Pri, Main Sec, Vol Pri, Vol Sec, RSI Pri, RSI Sec]
    if len(axes) > 4:
        axes[4].legend(['RSI'], loc='upper left')

    # Save the chart
    fig.savefig(output_path)


def format_large_number(value):
    """Formats large numbers into billions or millions with a dollar sign."""
    if value is None or value == 'N/A' or not isinstance(value, (int, float)):
        return value
    
    abs_val = abs(value)
    if abs_val >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs_val >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.2f}"


def get_stock_metrics(ticker: str) -> str:
    """
    Retrieves and summarizes key financial metrics for a given stock ticker using yfinance.

    This function fetches earnings data for the last 4 quarters and last 2 years, along with
    key financial metrics from the stock's info. It calculates CAGR for revenue and net income
    over the last 4 quarters and formats and returns a summary string.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        A formatted string containing summarized financial metrics including revenue, net profit,
        growth, CAGR for revenue and net income, P/E ratio, P/S ratio, market cap, debt,
        debt-to-equity ratio, and earnings data.
    """
    stock = yf.Ticker(ticker)

    # Get quarterly income statement for the last 4 quarters
    quarterly_income_stmt = stock.quarterly_income_stmt
    last_4_quarters = quarterly_income_stmt.iloc[:, :4] if quarterly_income_stmt is not None and not quarterly_income_stmt.empty and quarterly_income_stmt.shape[1] >= 4 else quarterly_income_stmt
    # Get annual income statement for the last 2 years
    annual_income_stmt = stock.income_stmt
    last_2_years = annual_income_stmt.iloc[:, :2] if annual_income_stmt is not None and not annual_income_stmt.empty and annual_income_stmt.shape[1] >= 2 else annual_income_stmt

    # Calculate CAGR for revenue and net income from last 4 quarters
    if last_4_quarters is not None and not last_4_quarters.empty and last_4_quarters.shape[1] >= 4:
        # Revenue CAGR
        if 'Total Revenue' in last_4_quarters.index:
            rev_series = last_4_quarters.loc['Total Revenue']
            beginning_rev = rev_series.iloc[-1]  # oldest quarter
            ending_rev = rev_series.iloc[0]      # newest quarter
            if beginning_rev > 0 and ending_rev > 0:
                cagr_rev = (ending_rev / beginning_rev)**(1/4) - 1
                cagr_rev_str = f"{cagr_rev * 100:.2f}%"
            else:
                cagr_rev_str = 'N/A'
        else:
            cagr_rev_str = 'N/A'
        # Net Income CAGR
        if 'Net Income' in last_4_quarters.index:
            inc_series = last_4_quarters.loc['Net Income']
            beginning_inc = inc_series.iloc[-1]  # oldest quarter
            ending_inc = inc_series.iloc[0]      # newest quarter
            if beginning_inc != 0 and ending_inc != 0:  # allow negative, but not zero
                cagr_inc = (ending_inc / beginning_inc)**(1/4) - 1
                cagr_inc_str = f"{cagr_inc * 100:.2f}%"
            else:
                cagr_inc_str = 'N/A'
        else:
            cagr_inc_str = 'N/A'
    else:
        cagr_rev_str = 'N/A'
        cagr_inc_str = 'N/A'



    # Get key metrics from info
    info = stock.info
    market_cap = format_large_number(info.get('marketCap', 'N/A'))
    pe_ratio = info.get('trailingPE', 'N/A')
    ps_ratio = info.get('priceToSalesTrailing12Months', 'N/A')
    total_debt = format_large_number(info.get('totalDebt', 'N/A'))
    debt_to_equity = info.get('debtToEquity', 'N/A')

    # Extract revenue, net income, and growth from annual income statement
    if last_2_years is not None and not last_2_years.empty:
        if 'Total Revenue' in last_2_years.index:
            revenue_series = last_2_years.loc['Total Revenue']
            revenue = format_large_number(revenue_series.iloc[0] if len(revenue_series) > 0 else 'N/A')
            if len(revenue_series) >= 2:
                rev_curr = revenue_series.iloc[0]
                rev_prev = revenue_series.iloc[1]
                growth = f"{((rev_curr - rev_prev) / rev_prev * 100):.2f}%" if rev_prev != 0 else 'N/A'
            else:
                growth = 'N/A'
        else:
            revenue = 'N/A'
            growth = 'N/A'
        if 'Net Income' in last_2_years.index:
            net_income_series = last_2_years.loc['Net Income']
            net_income = format_large_number(net_income_series.iloc[0] if len(net_income_series) > 0 else 'N/A')
        else:
            net_income = 'N/A'
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
Revenue CAGR (4 Quarters): {cagr_rev_str}
Net Income CAGR (4 Quarters): {cagr_inc_str}

"""
# Quarterly Earnings (Last 4 Quarters):
# {last_4_quarters.to_string(index=True) if last_4_quarters is not None else 'N/A'}

# Annual Earnings (Last 2 Years):
# {last_2_years.to_string(index=True) if last_2_years is not None else 'N/A'}

    return summary
