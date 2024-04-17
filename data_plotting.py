import matplotlib.pyplot as plt


def create_and_save_plot(data, ticker, period, filename=None):
    try:
        fig, axs = plt.subplots(3, 1, figsize=(18, 12))

        # График цены закрытия и скользящего среднего
        axs[0].plot(data.index, data['Close'], label='Close Price', color='blue')
        axs[0].plot(data.index, data['Moving_Average'], label='Moving Average', color='orange')
        axs[0].set_ylabel('Price')
        axs[0].set_title(f"{ticker} Stock Price and Moving Average")

        # График RSI
        axs[1].plot(data.index, data['RSI'], label='RSI', color='purple')
        axs[1].axhline(70, color='r', linestyle='--')
        axs[1].axhline(30, color='g', linestyle='--')
        axs[1].set_ylabel('RSI')
        axs[1].set_title(f"{ticker} Relative Strength Index (RSI)")

        # График MACD
        axs[2].plot(data.index, data['MACD'], label='MACD', color='blue')
        axs[2].plot(data.index, data['Signal_Line'], label='Signal Line', color='orange')
        axs[2].set_ylabel('MACD')
        axs[2].set_title(f"{ticker} Moving Average Convergence Divergence (MACD)")

        plt.xlabel("Date")
        plt.legend()

        if filename is None:
            filename = f"{ticker}_{period}_combined_chart.png"

        plt.savefig(filename)
        print(f"Combined chart saved as {filename}")
    except Exception as e:
        print(f"\nError creating and saving combined chart: {e}")
