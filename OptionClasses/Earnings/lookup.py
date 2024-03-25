import requests
import pandas as pd
from UseFunctions.date_time import two_date_period, previous_day, get_date_next_friday
from StockClasses.single_stock import SingleStock
from OptionClasses.Contracts.contract_spread import ContractSpread
from OptionClasses.Strategies.straddle import StraddleStrategy


class EarningsLookup:
    def __init__(self, from_date: str, to_date: str, report_time: str = 'any', remove_empties: bool = True,
                 api_key: str = 'sS3gwZ7cycpxe9G7JSAmwigdeOjvN2B4') -> None:
        self.from_date = from_date
        self.to_date = to_date
        self.report_time = report_time
        self.remove_empties = remove_empties
        self.api_key = api_key
        self.raw_data = self._get_earnings()
        self.earnings_output = self._clean_data()

    def _get_earnings(self) -> dict or None:
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={self.from_date}&to={self.to_date}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 401:
            print("Unauthorized earnings API access. Check your API key.")
            return None

        return response.json()

    def _clean_data(self):
        if self.report_time.lower() == 'any':
            filtered_data = self.raw_data
        else:
            filtered_data = [i for i in self.raw_data if i.get('time') == self.report_time.lower()]

        clean_data = [i for i in filtered_data if
                      {'date', 'symbol', 'time', 'eps', 'revenueEstimated', 'revenue'}.issubset(
                          i.keys()) and '.' not in i.get('symbol', '') and (
                              not self.remove_empties or all(v is not None for v in i.values()))]

        return pd.DataFrame(clean_data)

    def get_specific_company(self, ticker: str) -> pd.DataFrame:
        return self.earnings_output[self.earnings_output['symbol'] == ticker.upper()]


class StrategyTestInputs:
    def __init__(self, tickers, entry_exit_period: tuple, lookup_period_months=3, report_time='any',
                 test_quantity: int = 1, per_contract_commission: float = 0.01,
                 polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.tickers = tickers
        self.lookup_period_months = lookup_period_months
        self.report_time = report_time
        self.to_search_date, self.from_search_date = two_date_period(lookup_period_months)
        self.entry_exit_period = entry_exit_period
        self.entry1, self.entry2, self.exit1, self.exit2 = self.entry_exit_period
        self.quantity = test_quantity
        self.per_contract_commission = per_contract_commission
        self.polygon_api_key = polygon_api_key
        self.search_criteria = self._get_search_criteria()
        self.inputs_list = self._get_inputs_list()

    def _get_search_criteria(self):
        earnings_lookup = EarningsLookup(from_date=self.from_search_date, to_date=self.to_search_date,
                                         report_time=self.report_time)
        earnings_output = earnings_lookup.earnings_output

        search_criteria = []

        for ticker in self.tickers:
            ticker_earnings = earnings_output[earnings_output['symbol'] == ticker.upper()]
            if not ticker_earnings.empty:
                search_criteria.extend(ticker_earnings.to_dict(orient='records'))

        return search_criteria

    def _get_inputs_list(self) -> list[dict]:
        inputs_list = []
        for company in self.search_criteria:
            try:
                underlying = company['symbol'].upper()
                trade_date = previous_day(company['date']) if company['time'] == 'bmo' else company['date']
                expiration_date = get_date_next_friday(trade_date)
                average_entry_underlying = SingleStock(ticker=underlying, from_date=trade_date, from_time=self.entry1,
                                                       to_date=trade_date, to_time=self.entry2,
                                                       fill_gaps=False).get_average_price()

                strike = ContractSpread(
                    underlying, current_underlying=average_entry_underlying,
                    expiration_date_gte=expiration_date,
                    date_as_of=trade_date).get_best_matched_contracts()[0]['strike_price']

                entry = {
                    'ticker': underlying,
                    'strike': strike,
                    'expiration_date': expiration_date,
                    'entry_date': trade_date,
                    'exit_date': trade_date,
                }

                inputs_list.append(entry)
            except TypeError:
                continue
            except KeyError:
                continue

        return inputs_list

    def aggregate_ticker_simulations(self) -> pd.DataFrame:
        all_simulations = []  # List to store all simulation DataFrames
        for input_company in self.inputs_list:
            try:
                sim_inputs = StraddleStrategy(ticker=input_company['ticker'],
                                              strike=input_company['strike'],
                                              expiration_date=input_company['expiration_date'],
                                              quantity=self.quantity,
                                              entry_date=input_company['entry_date'],
                                              exit_date=input_company['exit_date'],
                                              strategy_type='long',
                                              entry_exit_period=self.entry_exit_period,
                                              timespan='minute',
                                              fill_gaps=True,
                                              per_contract_commission=self.per_contract_commission,
                                              multiplier=1,
                                              polygon_api_key=self.polygon_api_key)

                simulation = sim_inputs.run_simulation()

                if simulation is not None:  # Check if simulation is not None
                    all_simulations.append(simulation)  # Append each simulation DataFrame to the list
            except KeyError:
                continue

        return pd.concat(all_simulations, ignore_index=True)  # Concatenate all simulation DataFrames


tickers = ['aapl', 'nvda', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk', 'jpm', 'wmt',
           'v', 'pg', 'ma', 'jnj', 'hd', 'intc', 'unh', 'baba', 't', 'crm',
           'ko', 'cmcsa', 'dis', 'nflx', 'pypl', 'pep', 'abt', 'adbe', 'nke', 'mcd',
           'hon', 'bud', 'tmus', 'axp', 'cost', 'vz', 'mrk', 'orcl', 'pfe', 'amgn',
           'abbv', 'mdt', 'dhr', 'now', 'crm', 'acb', 'twtr', 'nclh', 'tsm',
           'amd', 'cat', 'ba', 'sbux', 'csco', 'fdx', 'ge', 'gm', 'hpe', 'ibm',
           'low', 'lmt', 'mo', 'sbux', 'ups', 'xom', 'snap', 'nke', 'tsn', 'ko',
           'pep', 'bud', 'mt', 'cl', 'k', 'gis', 'clx', 'pg', 'pg', 'ko',
           'pep', 'mo', 'bmy', 'gild', 'abt', 'dhr', 'tgt', 'wba', 'mnst',
           'kmb', 'cost', 'tjx', 'pm', 'mdlz', 'cl', 'k', 'avgo', 'txn', 'mu']


x = StrategyTestInputs(tickers, entry_exit_period=('10:30:00', '11:30:00', '15:30:00', '16:00:00'))
sims = x.aggregate_ticker_simulations()

# test = EarningsLookup(from_date='2023-11-12', to_date='2024-03-21', report_time='amc')
# print(test.get_specific_company(ticker='AAPL'))
