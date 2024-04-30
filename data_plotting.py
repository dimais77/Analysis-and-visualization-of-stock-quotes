import os
import matplotlib.pyplot as plt
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_and_save_plot(data: pd.DataFrame, ticker: str, period: str, start_date: str, end_date: str,
                         std_deviation: float, style: str = None, filename: str = None) -> None:
    """
    Создает и сохраняет интерактивный график на основе данных о биржевой акции.

    Parameters:
        data (pd.DataFrame): Данные о биржевой акции в формате DataFrame.
        ticker (str): Тикер акции.
        period (str): Период для данных.
        start_date (str): Дата начала анализа.
        end_date (str): Дата окончания анализа.
        std_deviation (float): Стандартное отклонение цены закрытия.
        style (str, optional): Стиль графика. По умолчанию None.
        filename (str, optional): Имя файла для сохранения графика. По умолчанию None.

    Returns:
        None
    """
    try:
        if style:
            plt.style.use(style)

        fig, axs = plt.subplots(3, 1, figsize=(18, 25))

        # График цены закрытия, скользящего среднего и стандартного отклонения
        axs[0].plot(data.index, data['Close'], label='Цена закрытия', color='blue')
        axs[0].plot(data.index, data['Moving_Average'], label='Скользящее среднее', color='orange')
        fill_label = 'Стандартное отклонение'
        axs[0].fill_between(data.index, data['Close'] - std_deviation, data['Close'] + std_deviation, color='lightblue',
                            alpha=0.5, label=fill_label)
        axs[0].set_ylabel('Цена')
        axs[0].set_title(f"\nЦены акций {ticker}, скользящее среднее и стандартное отклонение\n", fontweight='bold',
                         fontsize=16)
        axs[0].legend()

        # График RSI
        axs[1].plot(data.index, data['RSI'], label='RSI', color='purple')
        axs[1].axhline(70, color='r', linestyle='--')
        axs[1].axhline(30, color='g', linestyle='--')
        axs[1].set_ylabel('RSI')
        axs[1].set_title(f"\nОтносительный индекс силы {ticker} (RSI)\n", fontweight='bold',
                         fontsize=16)
        axs[1].legend()

        # График MACD
        axs[2].plot(data.index, data['MACD'], label='MACD', color='blue')
        axs[2].plot(data.index, data['Signal_Line'], label='Сигнальная линия', color='orange')
        axs[2].set_ylabel('MACD')
        axs[2].set_title(f"\nСхождение и расхождение скользящих средних {ticker} (MACD)\n", fontweight='bold',
                         fontsize=16)
        axs[2].legend()

        fig.suptitle(f"Анализ акций {ticker}", fontsize=20, fontweight='bold')  # Общий заголовок

        plt.xlabel("Дата")

        if filename is None:
            filename = f"{ticker}_{period}_chart.png" if period else f"{ticker}_{start_date}_to_{end_date}_chart.png"

        plt.savefig(filename)
        print(f"Графики сохранены в {filename}")

        # Проверка наличия файла
        if os.path.exists(filename):
            print(f"Файл {filename} был успешно создан.")
        else:
            print(f"Ошибка: Файл {filename} не был создан.")
    except Exception as e:
        print(f"\nОшибка при создании и сохранении графика: {e}")



def create_and_show_plot(data: pd.DataFrame, ticker: str, std_deviation: float) -> None:
    """
    Создает и отображает в браузере интерактивные графики цен акций, скользящего среднего, стандартного отклонения,
    RSI и MACD для указанного тикера.

    Parameters:
        data (pd.DataFrame): Данные об акциях, включая цены закрытия, скользящее среднее, RSI и MACD.
        ticker (str): Символ акции для отображения на графике.
        std_deviation (float): Стандартное отклонение для построения верхней и нижней границы стандартного отклонения.

    Returns:
        None

    В случае возникновения ошибки при создании графика, выводит сообщение об ошибке.
    """
    try:
        # Создание макета с тремя графиками
        fig = make_subplots(rows=3, cols=1, subplot_titles=(
            f"Цены акций {ticker}, скользящее среднее и стандартное отклонение",
            f"Относительный индекс силы {ticker} (RSI)",
            f"Схождение и расхождение скользящих средних {ticker} (MACD)"
        ))

        # График цены закрытия, скользящего среднего и стандартного отклонения
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Скользящее среднее'),
                      row=1, col=1)
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Close'] + std_deviation, mode='lines', name='Верхнее станд. откл.',
                       fill=None), row=1, col=1)
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Close'] - std_deviation, mode='lines', name='Нижнее станд. откл.',
                       fill='tonexty'), row=1, col=1)

        # График RSI
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'), row=2, col=1)
        fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1)

        # График MACD
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['Signal_Line'], mode='lines', name='Сигнальная линия'), row=3,
                      col=1)

        # Общие настройки графика
        fig.update_layout(
            height=1200,
            width=800,
            title_text=f"Анализ акций {ticker}",
            title_font_size=30,  # Размер шрифта заголовка
            title_x=0.5  # Положение заголовка по горизонтали (0.5 - по центру)
        )
        fig.update_xaxes(title_text="Дата", row=3, col=1)

        filename = f"{ticker}_interactive_chart.html"

        # Сохранение графика в HTML и открытие его в браузере
        fig.write_html(filename)

        # Открытие графика в браузере
        fig.show()

    except Exception as e:
        print(f"\nОшибка при создании графика: {e}")
