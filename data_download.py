import yfinance as yf


def fetch_stock_data(ticker, period='1mo', start=None):
    # Функция отвечает за загрузку данных об акциях за период из yfinance.
    try:
        if start is not None:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, start=start)
        else:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
        print(data)
        return data
    except Exception as e:
        print(f"\nОшибка при получении данных для тикера {ticker}: {e}")
        return None


def add_moving_average(data, window_size=5):
    # Функция отвечает за  расчёт скользящего среднего цены закрытия акций
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data, ticker):
    # Функция вычисляет и выводит в консоль среднюю цену закрытия акций за заданный период.

    avr_price = data['Close'].mean()
    avr_price_rounded = round(avr_price, 6)

    start_date = data.index.min().strftime('%Y-%m-%d')
    end_date = data.index.max().strftime('%Y-%m-%d')

    print(
        f'\nСредняя цена закрытия акции "{ticker}" за период <{start_date}...{end_date}> '
        f'составила: {avr_price_rounded}')


def notify_if_strong_fluctuations(data, ticker, threshold=5):
    # Функция вычисляет максимальное и минимальное значения цены закрытия и сравнивает с заданным порогом
    # (по умолчанию порог threshold=5). Если разница превышает порог, пользователь получит уведомление.
    max_closing_price = data['Close'].max()
    min_closing_price = data['Close'].min()
    fluctuation = ((max_closing_price - min_closing_price) / min_closing_price) * 100
    fluctuation_rounded = round(fluctuation, 1)
    if fluctuation_rounded > threshold:
        print(
            f'За указанный период отмечается сильное колебание цены закрытия акций "{ticker}": {fluctuation_rounded}%')


def export_data_to_csv(data, filename):
    #  Функция записывает данные в CSV файл
    data.to_csv(filename)
    print(f"\nДанные по запросу сохранены в файл {filename}")
