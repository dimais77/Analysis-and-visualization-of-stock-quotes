import unittest
import pandas as pd
from unittest.mock import patch
from data_download import fetch_stock_data, add_moving_average, calculate_and_display_average_price, calculate_rsi, \
    calculate_macd, notify_if_strong_fluctuations, export_data_to_csv
import tempfile


class TestDataDownload(unittest.TestCase):

    @patch('data_download.yf.Ticker')
    def test_fetch_stock_data(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame({'Close': [10, 20, 30, 40, 50]})
        data = fetch_stock_data('AAPL', '1d')
        self.assertIsInstance(data, pd.DataFrame)

    def test_add_moving_average(self):
        data = pd.DataFrame({'Close': [10, 20, 30, 40, 50]})
        data_with_ma = add_moving_average(data, window_size=3)
        self.assertIn('Moving_Average', data_with_ma.columns)

    @patch('builtins.print')
    def test_calculate_and_display_average_price(self, mocked_print):
        data = pd.DataFrame({'Close': [10, 20, 30, 40, 50]}, index=pd.date_range('2022-01-01', periods=5))
        calculate_and_display_average_price(data, 'AAPL')
        mocked_print.assert_called()

    @patch('builtins.print')
    def test_notify_if_strong_fluctuations(self, mocked_print):
        data = pd.DataFrame({'Close': [10, 20, 30, 40, 50]})
        notify_if_strong_fluctuations(data, 'AAPL', 5)
        mocked_print.assert_called()

    @patch('builtins.print')
    def test_export_data_to_csv(self, mocked_print):
        data = pd.DataFrame({'Close': [10, 20, 30, 40, 50]})
        with tempfile.NamedTemporaryFile() as tf:
            export_data_to_csv(data, tf.name)
            mocked_print.assert_called_with('\nДанные по запросу сохранены в файл ' + tf.name)
            result_data = pd.read_csv(tf.name)
            pd.testing.assert_frame_equal(data, result_data.iloc[:, 1:],
                                          check_dtype=False)  # Adjusting columns due to index

    def test_calculate_rsi(self):
        data = pd.DataFrame({'Close': [10, 20, 15, 25, 30]})
        data_with_rsi = calculate_rsi(data)
        self.assertIn('RSI', data_with_rsi.columns)

    def test_calculate_macd(self):
        data = pd.DataFrame({'Close': [10, 20, 15, 25, 30]})
        data_with_macd = calculate_macd(data)
        self.assertIn('MACD', data_with_macd.columns)
        self.assertIn('Signal_Line', data_with_macd.columns)


if __name__ == '__main__':
    unittest.main()
