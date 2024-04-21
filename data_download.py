import yfinance as yf
from typing import Optional, Union
import pandas as pd


def fetch_stock_data(ticker: str, period: str, start: Optional[str] = None, end: Optional[str] = None) -> Union[
    pd.DataFrame, None]:
    """
    Fetches stock data for a given ticker from Yahoo Finance.

    Parameters:
        ticker (str): Stock symbol to fetch data for.
        period (str): Data period.
        start (str, optional): Start date for the data period.
        end (str, optional): End date for the data period.

    Returns:
        pd.DataFrame: Stock data or None if an error occurs.
    """
    try:
        if start is not None:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, start=start, end=end)
        else:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
        print(data)
        return data
    except Exception as e:
        print(f"\nОшибка при получении данных для тикера {ticker}: {e}")
        return None


def add_moving_average(data, window_size=5):
    try:
        data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
        return data
    except Exception as e:
        print(f"\nОшибка при добавлении скользящего среднего: {e}")
        return None


def calculate_and_display_average_price(data, ticker):
    try:
        avr_price = data['Close'].mean()
        avr_price_rounded = round(avr_price, 6)

        start_date = data.index.min().strftime('%Y-%m-%d')
        end_date = data.index.max().strftime('%Y-%m-%d')

        print(
            f'\nСредняя цена закрытия акции "{ticker}" за период <{start_date}...{end_date}> '
            f'составила: {avr_price_rounded}')
    except Exception as e:
        print(f"\nОшибка при вычислении и отображении средней цены: {e}")


def notify_if_strong_fluctuations(data, ticker, threshold=5):
    try:
        max_closing_price = data['Close'].max()
        min_closing_price = data['Close'].min()
        fluctuation = ((max_closing_price - min_closing_price) / min_closing_price) * 100
        fluctuation_rounded = round(fluctuation, 1)
        if fluctuation_rounded > threshold:
            print(
                f'За указанный период отмечается сильное колебание '
                f'цены закрытия акций "{ticker}": {fluctuation_rounded}%')
    except Exception as e:
        print(f"\nОшибка при определении сильных колебаний: {e}")


def export_data_to_csv(data, filename):
    try:
        data.to_csv(filename)
        print(f"\nДанные по запросу сохранены в файл {filename}")
    except Exception as e:
        print(f"\nОшибка при экспорте данных в CSV: {e}")


def calculate_rsi(data, window_size=14):
    try:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        data['RSI'] = rsi
        return data
    except Exception as e:
        print(f"\nОшибка при расчёте RSI: {e}")
        return None


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    try:
        short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
        data['MACD'] = short_ema - long_ema
        data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        return data
    except Exception as e:
        print(f"\nОшибка при расчёте MACD: {e}")
        return None
