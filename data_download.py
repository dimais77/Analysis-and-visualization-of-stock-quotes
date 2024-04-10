import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data, ticker):
    # Функция вычисляет и выводит в консоль среднюю цену закрытия акций за заданный период.

    avr_price = data['Close'].mean()
    avr_price_rounded = round(avr_price, 6)

    start_date = data.index.min().strftime('%Y-%m-%d')
    end_date = data.index.max().strftime('%Y-%m-%d')

    print(f'Средняя цена закрытия акции "{ticker}" за период <{start_date}...{end_date}>: {avr_price_rounded}')
