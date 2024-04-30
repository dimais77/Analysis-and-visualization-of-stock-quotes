import os

import yfinance as yf
from typing import Optional, Union
import pandas as pd


def fetch_stock_data(ticker: str, period: str, start: Optional[str] = None,
                     end: Optional[str] = None) -> Union[pd.DataFrame, None]:
    """
    Получает данные об акциях для указанного тикера из Yahoo Finance.

    Parameters:
        ticker (str): Символ акции, для которой нужно получить данные.
        period (str): Период данных.
        start (str, optional): Начальная дата периода данных.
        end (str, optional): Конечная дата периода данных.

    Returns:
        pd.DataFrame: Данные об акциях или None в случае ошибки.
    """
    try:
        stock = yf.Ticker(ticker)
        if start is not None:
            data = stock.history(period=period, start=start, end=end)
        else:
            data = stock.history(period=period)
        print(data)
        return data
    except Exception as e:
        print(f"\nОшибка при получении данных для тикера {ticker}: {e}")
        return None


def add_moving_average(data: pd.DataFrame, window_size: int = 5) -> Union[pd.DataFrame, None]:
    """
    Считает и добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций с Yahoo Finance.
        window_size (int): Размер окна для вычисления скользящего среднего.

    Returns:
        pd.DataFrame: Данные об акциях с добавленным столбцом Moving_Average или None в случае ошибки.
    """
    try:
        data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
        return data
    except Exception as e:
        print(f"\nОшибка при добавлении скользящего среднего: {e}")
        return None


def calculate_and_display_average_price(data: pd.DataFrame, ticker: str) -> None:
    """
    Вычисляет и выводит в консоль среднюю цену закрытия акций за заданный период.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций.
        ticker (str): Тикер акции.

    Returns:
        None
    """
    try:
        avr_price = data['Close'].mean()
        avr_price_rounded = round(avr_price, 6)

        start_date = data.index.min().strftime('%Y-%m-%d')
        end_date = data.index.max().strftime('%Y-%m-%d')

        print(
            f'\nСредняя цена закрытия акции "{ticker}" за период <{start_date}...{end_date}> '
            f'составила: {avr_price_rounded}')
        return avr_price_rounded
    except Exception as e:
        print(f"\nОшибка при вычислении и отображении средней цены: {e}")


def notify_if_strong_fluctuations(data: pd.DataFrame, ticker: str, threshold=5) -> None:
    """
    Вычисляет максимальное и минимальное значения цены закрытия и сравнивает с заданным порогом.
    Если разница превышает порог, выводит уведомление.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций.
        ticker (str): Тикер акции.
        threshold (int): Порог для определения сильных колебаний.

    Returns:
        None
    """
    try:
        max_closing_price = data['Close'].max()
        min_closing_price = data['Close'].min()
        fluctuation = ((max_closing_price - min_closing_price) / min_closing_price) * 100
        fluctuation_rounded = round(fluctuation, 1)
        if fluctuation_rounded > threshold:
            print(
                f'За указанный период отмечается сильное колебание '
                f'цены закрытия акций "{ticker}": {fluctuation_rounded}%')
            return fluctuation_rounded
    except Exception as e:
        print(f"\nОшибка при определении сильных колебаний: {e}")


def export_data_to_csv(data: pd.DataFrame, filename: str) -> None:
    """
    Экспортирует данные в формате CSV.

    Parameters:
        data (pd.DataFrame): Данные для экспорта.
        filename (str): Имя файла для сохранения данных.

    Returns:
        None
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Параметр 'data' должен быть объектом pd.DataFrame")
        if not isinstance(filename, str):
            raise TypeError("Параметр 'filename' должен быть строкой")

        if os.path.exists(filename):
            print(f"Файл {filename} уже существует. Перезаписать?")

        data.to_csv(filename)
        print(f"\nДанные по запросу сохранены в файл {filename}")
    except Exception as e:
        print(f"\nОшибка при экспорте данных в CSV: {e}")


def calculate_rsi(data: pd.DataFrame, window_size=14):
    """
    Принимает DataFrame с данными о цене закрытия акций, вычисляет RSI (Relative Strength Index) и добавляет его в
    DataFrame.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций.
        window_size (int): Размер окна для вычисления RSI.

    Returns:
        pd.DataFrame: DataFrame с добавленным столбцом RSI или None в случае ошибки.
    """
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


def calculate_macd(data: pd.DataFrame, short_window=12, long_window=26, signal_window=9):
    """
    Принимает DataFrame с данными о цене закрытия акций, вычисляет MACD (Moving Average Convergence Divergence) и
    линию сигнала.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций.
        short_window (int): Короткое окно для вычисления EMA.
        long_window (int): Длинное окно для вычисления EMA.
        signal_window (int): Окно для вычисления линии сигнала.

    Returns:
        pd.DataFrame: DataFrame с добавленными столбцами MACD и Signal_Line или None в случае ошибки.
    """
    try:
        short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
        data['MACD'] = short_ema - long_ema
        data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        return data
    except Exception as e:
        print(f"\nОшибка при расчёте MACD: {e}")
        return None


def calculate_standard_deviation(data: pd.DataFrame):
    """
    Принимает DataFrame с данными о цене закрытия акций и вычисляет стандартное отклонение.

    Parameters:
        data (pd.DataFrame): Данные о цене закрытия акций.

    Returns:
        float: Значение стандартного отклонения или None в случае ошибки.
    """
    try:
        std_deviation = data['Close'].std(ddof=1)
        print(f'\nСтандартное отклонение цены закрытия: {std_deviation}')
        return std_deviation
    except Exception as e:
        print(f"\nОшибка при расчете стандартного отклонения: {e}")
        return None
