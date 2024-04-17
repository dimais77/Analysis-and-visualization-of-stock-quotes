import data_download as dd
import data_plotting as dplt
from datetime import datetime


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet "
        "Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, "
        "макс. (1d, 1w, 1mo, 1y, start_y, max")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    if period == 'start_y':
        start_date = datetime(datetime.now().year, 1, 1)
    else:
        start_date = None
    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start=start_date)

    if stock_data is not None:
        # Add moving average to the data
        stock_data = dd.add_moving_average(stock_data)

        # Displays average closing stock price for the period
        dd.calculate_and_display_average_price(stock_data, ticker)

        # Displays notification if fluctuations exceed a specified threshold
        dd.notify_if_strong_fluctuations(stock_data, ticker)  # По умолчанию threshold=5, либо укажите иной %

        # Export data to csv file
        filename = f'{ticker}_{period}_stock_data.csv'
        dd.export_data_to_csv(stock_data, filename)

        # Calculate and plot data, moving average, RSI, MACD
        stock_data_with_indicators = dd.calculate_rsi(stock_data, window_size=5)
        stock_data_with_indicators = dd.calculate_macd(stock_data_with_indicators, short_window=12, long_window=26,
                                                       signal_window=9)
        dplt.create_and_save_plot(stock_data_with_indicators, ticker, period, filename=None)
    else:
        print(
            "Данные об акциях не были получены. Пожалуйста, проверьте введенные данные и повторите попытку.")


if __name__ == "__main__":
    main()
