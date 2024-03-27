import requests
import pandas as pd
from UseFunctions.date_time import two_date_period, previous_day, get_date_next_friday, next_third_friday
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
                 test_quantity: int = 1, per_contract_commission: float = 0.01, lookup_from: str = '',
                 polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.tickers = tickers
        self.lookup_period_months = lookup_period_months
        self.report_time = report_time
        self.to_search_date, self.from_search_date = two_date_period(lookup_period_months, lookup_from)
        self.entry_exit_period = entry_exit_period
        self.entry1, self.entry2, self.exit1, self.exit2 = self.entry_exit_period
        self.quantity = test_quantity
        self.per_contract_commission = per_contract_commission
        self.polygon_api_key = polygon_api_key
        self.errors_list = []
        self.tested_tickers = []
        self.search_criteria = self._get_search_criteria()
        self.inputs_list = self._get_inputs_list()

    def _get_search_criteria(self):
        earnings_lookup = EarningsLookup(from_date=self.from_search_date, to_date=self.to_search_date,
                                         report_time=self.report_time)
        earnings_output = earnings_lookup.earnings_output

        search_criteria = []
        errors_list = []

        for ticker in self.tickers:
            ticker_earnings = earnings_output[earnings_output['symbol'] == ticker.upper()]
            if not ticker_earnings.empty:
                search_criteria.extend(ticker_earnings.to_dict(orient='records'))
            else:
                errors_list.append({'ticker': ticker, 'error': 'Earnings Calendar Search'})

        self.errors_list.extend(errors_list)

        return search_criteria

    def _get_inputs_list(self) -> (list[dict], list[dict]):
        inputs_list = []
        errors_list = []
        for company in self.search_criteria:
            underlying = company['symbol'].upper()
            trade_date = previous_day(company['date']) if company['time'] == 'bmo' else company['date']
            expiration_date = get_date_next_friday(trade_date)
            try:
                average_entry_underlying = SingleStock(ticker=underlying, from_date=trade_date, from_time=self.entry1,
                                                       to_date=trade_date, to_time=self.entry2,
                                                       fill_gaps=False).get_average_price()
            except TypeError:
                errors_list.append({'ticker': underlying, 'error': 'TypeError Stock'})
                continue
            except KeyError:
                errors_list.append({'ticker': underlying, 'error': 'KeyError Stock'})
                continue
            except ValueError:
                errors_list.append({'ticker': underlying, 'error': 'ValueError Stock'})
                continue
            try:
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

            except ValueError:
                try:
                    strike = ContractSpread(
                        underlying, current_underlying=average_entry_underlying,
                        expiration_date_gte=next_third_friday(trade_date),
                        date_as_of=trade_date).get_best_matched_contracts()[0]['strike_price']
                except ValueError:
                    errors_list.append({'ticker': underlying, 'error': 'ValueError Spread'})
                    continue

                entry = {
                    'ticker': underlying,
                    'strike': strike,
                    'expiration_date': expiration_date,
                    'entry_date': trade_date,
                    'exit_date': trade_date,
                }

                inputs_list.append(entry)
            except TypeError:
                errors_list.append({'ticker': underlying, 'error': 'TypeError Spread'})
                continue
            except KeyError:
                errors_list.append({'ticker': underlying, 'error': 'KeyError Spread'})
                continue

        self.errors_list.extend(errors_list)

        return inputs_list

    def aggregate_ticker_simulations(self) -> (pd.DataFrame, list[dict]):
        all_simulations = []  # List to store all simulation DataFrames`
        errors_list = []
        tested_tickers = []
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
                    tested_tickers.append({
                        'ticker': input_company['ticker'],
                        'trade_date': input_company['entry_date'],
                        'strike': input_company['strike'],
                        'expiration': input_company['expiration_date'],
                    })
            except KeyError:
                errors_list.append({'ticker': input_company['ticker'], 'error': 'KeyError Strategy'})
                continue

        self.tested_tickers.extend(tested_tickers)

        full_sims = pd.concat(all_simulations, ignore_index=True)  # Concatenate all simulation DataFrames

        self.errors_list.extend(errors_list)

        return full_sims



