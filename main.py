import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet "
        "Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, "
        "макс. (1d, 1w, 1mo, 1y, start_y, max)")

    # Запрос тикера акции
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Проверка наличия тикера перед запросом периода
    if not ticker:
        print("Тикер акции не был введен. Повторите попытку.")
        return

    # Запрос периода для данных
    period = input("Введите период для данных (например, '1mo' для одного месяца), либо пропустите (enter) для ввода "
                   "конкретных дат: ")

    start_date = None
    end_date = None

    # Если период не указан, запрашиваем конкретные даты
    if not period:
        start_date = input("Введите дату начала анализа в формате 'ГГГГ-ММ-ДД' (например, '2022-01-01'): ")
        end_date = input("Введите дату окончания анализа в формате 'ГГГГ-ММ-ДД' (например, '2022-12-31'): ")

    # Получение данных о биржевой акции
    stock_data = dd.fetch_stock_data(ticker, period, start=start_date, end=end_date)

    if stock_data is not None:
        # Добавление скользящего среднего к данным
        stock_data = dd.add_moving_average(stock_data)

        # Отображение средней цены закрытия акции за указанный период
        dd.calculate_and_display_average_price(stock_data, ticker)

        # Отображение уведомления, если колебания превышают заданный порог
        dd.notify_if_strong_fluctuations(stock_data, ticker)

        # Экспорт данных в файл CSV
        filename = f'{ticker}_{period if period else f"{start_date}_to_{end_date}"}_stock_data.csv'
        dd.export_data_to_csv(stock_data, filename)

        # Расчет и построение графиков данных, скользящего среднего, RSI, MACD
        stock_data_with_indicators = dd.calculate_rsi(stock_data, window_size=5)
        stock_data_with_indicators = dd.calculate_macd(stock_data_with_indicators, short_window=12, long_window=26,
                                                       signal_window=9)

        # Запрос выбора стиля графика
        style = input("По желанию введите стиль графика (например, 'classic', 'ggplot', 'bmh', 'fivethirtyeight'): ")

        dplt.create_and_save_plot(stock_data_with_indicators, ticker, period, start_date, end_date, style=style)
    else:
        print(
            "Данные об акциях не были получены. Пожалуйста, проверьте введенные данные и повторите попытку.")


if __name__ == "__main__":
    main()
