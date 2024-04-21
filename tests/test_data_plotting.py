import unittest
import pandas as pd
import os
from unittest.mock import patch
from data_plotting import create_and_save_plot


class TestDataPlotting(unittest.TestCase):

    def test_create_and_save_plot_with_filename(self):
        data = pd.DataFrame({
            'Close': [10, 20, 30, 40, 50],
            'Moving_Average': [15, 25, 35, 45, 55],
            'RSI': [50, 60, 70, 80, 90],
            'MACD': [5, 10, 15, 20, 25],
            'Signal_Line': [3, 8, 13, 18, 23]
        }, index=pd.date_range('2022-01-01', periods=5))
        ticker = 'AAPL'
        period = '2022'
        start_date = '2022-01-01'
        end_date = '2022-01-05'
        filename = 'test_chart.png'

        with patch('builtins.print') as mocked_print, patch('matplotlib.pyplot.savefig') as mocked_savefig:
            create_and_save_plot(data, ticker, period, start_date, end_date, filename)

            expected_filename = filename
            mocked_savefig.assert_called_with(expected_filename)

            expected_output = f"Ошибка: Файл {filename} не был создан."
            mocked_print.assert_called_with(expected_output)

            self.assertFalse(os.path.exists(filename))  # Проверяем, что файл не был создан

    def test_create_and_save_plot_no_filename(self):
        data = pd.DataFrame({
            'Close': [10, 20, 30, 40, 50],
            'Moving_Average': [15, 25, 35, 45, 55],
            'RSI': [50, 60, 70, 80, 90],
            'MACD': [5, 10, 15, 20, 25],
            'Signal_Line': [3, 8, 13, 18, 23]
        }, index=pd.date_range('2022-01-01', periods=5))
        ticker = 'AAPL'
        period = '2022'
        start_date = '2022-01-01'
        end_date = '2022-01-05'

        with patch('builtins.print') as mocked_print, patch('matplotlib.pyplot.savefig') as mocked_savefig:
            create_and_save_plot(data, ticker, period, start_date, end_date)

            expected_filename = f"{ticker}_{period}_chart.png" if period else f"{ticker}_{start_date}_to_{end_date}_chart.png"
            mocked_savefig.assert_called_with(expected_filename)

            expected_output = f"Ошибка: Файл {expected_filename} не был создан."
            mocked_print.assert_called_with(expected_output)

            self.assertFalse(os.path.exists(expected_filename))  # Проверяем, что файл не был создан


if __name__ == '__main__':
    unittest.main()
