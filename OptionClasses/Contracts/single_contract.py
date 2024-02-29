from UseFunctions.date_time import to_unix_time
from UseFunctions.entries import create_options_ticker
import requests
import pandas as pd


class SingleOptionsContract:
    def __init__(self, ticker: str, strike: float, expiration_date: str, is_call: bool) -> None:
        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.is_call = is_call

    def get_data(self, from_date: str, to_date: str, window_start_time: str, window_end_time: str,
                 timespan: str, multiplier: int = 1,
                 polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz') -> pd.DataFrame or None:
        from_date = to_unix_time(f'{from_date} {window_start_time}')
        to_date = to_unix_time(f'{to_date} {window_end_time}')

        options_ticker = create_options_ticker(ticker=self.ticker,
                                               strike=self.strike,
                                               expiration_date=self.expiration_date,
                                               contract_type=self.is_call)

        headers = {"Authorization": f"Bearer {polygon_api_key}"}
        options_endpoint = f"https://api.polygon.io/v2/aggs/ticker/{options_ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

        options_response_raw = requests.get(options_endpoint, headers=headers).json()
        options_response = options_response_raw['results'] if options_response_raw['queryCount'] != 0 else None
        options_data = pd.DataFrame(options_response)

        return options_data

    def get_stock_prices(self, from_date: str, to_date: str, window_start_time: str, window_end_time: str,
                         timespan: str, multiplier: int = 1,
                         polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz') -> pd.DataFrame or None:
        from_date = to_unix_time(f'{from_date} {window_start_time}')
        to_date = to_unix_time(f'{to_date} {window_end_time}')

        headers = {"Authorization": f"Bearer {polygon_api_key}"}
        stock_endpoint = f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

        stock_response_raw = requests.get(stock_endpoint, headers=headers).json()
        stock_response = stock_response_raw['results'] if stock_response_raw['queryCount'] != 0 else None
        stock_data = pd.DataFrame(stock_response)

        return stock_data


# test_contract = SingleOptionsContract("aapl", 185, '2024-02-16', True)
# test_contract_data = test_contract.get_stock_prices(from_date='2024-02-12', to_date='2024-02-12',
#                                                     window_start_time='09:30:00', window_end_time='16:30:00',
#                                                     timespan='minute')
# print(test_contract_data.columns)
