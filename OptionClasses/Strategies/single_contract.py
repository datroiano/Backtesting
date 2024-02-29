from OptionClasses.Contracts.single_contract import SingleOptionsContract
import pandas as pd
from datetime import datetime, timedelta, time


class SingleContractStrategy:
    def __init__(self,
                 ticker: str, strike: int or float, expiration_date: str, quantity: int, entry_date: str,
                 exit_date: str, is_call: bool, entry_exit_period: tuple, strategy_type: str = 'long',
                 fill_gaps: bool = True, with_stock_prices: bool = True,
                 timespan: str = 'minute', per_contract_commission: float = 0.00,
                 closed_market_period: tuple = ('09:30:00', '16:00:00'), pricing_criteria: str = 'h',
                 multiplier: int = 1, polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz') -> None:

        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.is_call = is_call
        self.multiplier = multiplier
        self.with_stock_prices = with_stock_prices
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period
        self.market_open, self.market_close = closed_market_period[0], closed_market_period[1]
        self.per_contract_commission = per_contract_commission
        self.quantity = quantity
        self.pricing_criteria = pricing_criteria
        self.strategy_type = False if strategy_type.upper() == 'SHORT' else True

        contract = SingleOptionsContract(ticker=self.ticker, strike=self.strike, expiration_date=self.expiration_date,
                                         is_call=self.is_call)

        self.contract_data = contract.get_data(from_date=self.entry_date, to_date=self.exit_date,
                                               window_start_time=self.entry_exit_period[0],
                                               window_end_time=self.entry_exit_period[3],
                                               timespan=self.timespan, multiplier=self.multiplier,
                                               polygon_api_key=self.polygon_api_key)

        self.contract_data = self._fill_gaps(self.contract_data) if fill_gaps else self.contract_data

        if with_stock_prices:
            self.stock_data = contract.get_stock_prices(from_date=self.entry_date, to_date=self.exit_date,
                                                        window_start_time=self.entry_exit_period[0],
                                                        window_end_time=self.entry_exit_period[3],
                                                        timespan=self.timespan, multiplier=self.multiplier,
                                                        polygon_api_key=self.polygon_api_key)

            self.stock_data = self._fill_gaps(self.stock_data)

            self.stock_data.rename(columns={'v': 'sv', 'o': 'so', 'c': 'sc', 'h': 'sh', 'l': 'sl',
                                            'n': 'sn', 'vw': 'svw'}, inplace=True)

            self.merged_data = pd.merge(self.contract_data, self.stock_data, on='t')

    def _fill_gaps(self, securities_data: pd.DataFrame) -> pd.DataFrame:
        trading_start_time = time(int(self.market_open[0:2]), int(self.market_open[3:5]))
        trading_end_time = time(int(self.market_close[0:2]), int(self.market_close[3:5]))

        filled_data = []

        time_spans = {
            "minute": timedelta(minutes=1),
            "hour": timedelta(hours=1),
            "day": timedelta(days=1),
            "second": timedelta(seconds=1)
        }
        interval = time_spans.get(self.timespan)

        if interval is None:
            raise ValueError("Invalid timespan specified")

        for i in range(len(securities_data)):
            filled_data.append(list(securities_data.iloc[i]))  # Append as list instead of dict
            if i < (len(securities_data) - 1):
                current_time = datetime.fromtimestamp(securities_data.iloc[i]['t'] / 1000)
                next_time = datetime.fromtimestamp(securities_data.iloc[i + 1]['t'] / 1000)
                while current_time + interval < next_time and (
                        trading_start_time <= current_time.time() <= trading_end_time):
                    current_time += interval
                    filled_data.append([
                        securities_data.iloc[i]['v'],
                        securities_data.iloc[i]['vw'],
                        securities_data.iloc[i]['c'],  # assuming the open is equal to the previous close
                        securities_data.iloc[i]['c'],
                        securities_data.iloc[i]['c'],
                        securities_data.iloc[i]['c'],
                        int(current_time.timestamp() * 1000),
                        0  # fill gap indicator
                    ])

        return pd.DataFrame(filled_data, columns=self.contract_data.columns)

    def run_simulation(self) -> pd.DataFrame or None:
        def extract_points(data, start_time, end_time):
            return data[(data['t'] >= start_time) & (data['t'] <= end_time)].to_dict('records')

        def calculate_simulated_trade(entry_point, exit_point):
            entry_contract_price = entry_point[self.pricing_criteria]
            entry_strategy_price = entry_contract_price * self.quantity
            exit_contract_price = exit_point[self.pricing_criteria]
            exit_strategy_price = exit_contract_price * self.quantity

            commission_paid = self.quantity * self.per_contract_commission
            contract_change_dollars = exit_contract_price - entry_contract_price
            contract_change_percent = contract_change_dollars / entry_contract_price

            if self.strategy_type:
                strategy_profit_dollars = exit_strategy_price - entry_strategy_price - (2 * commission_paid)
            else:
                strategy_profit_dollars = entry_strategy_price - exit_strategy_price - (2 * commission_paid)

            strategy_profit_percent = strategy_profit_dollars / entry_strategy_price

            stock_price_change = (exit_point.get(f"s{self.pricing_criteria}", None) -
                                  entry_point.get(f"s{self.pricing_criteria}", None))

            stock_price_change_percent = stock_price_change / entry_point.get(f"s{self.pricing_criteria}", None)

            return {
                'entry_time': entry_point['t'],
                'entry_contract_price': entry_contract_price,
                'entry_stock_price': entry_point.get(f"s{self.pricing_criteria}", None),
                'entry_strategy_price': entry_strategy_price,
                'entry_volume': entry_point['v'],
                'entry_volume_weighted': entry_point['vw'],
                'entry_stock_volume': entry_point.get('sv', None),
                'entry_stock_volume_weighted': entry_point.get('svw', None),
                'entry_runs': entry_point['n'],
                'exit_time': exit_point['t'],
                'exit_contract_price': exit_contract_price,
                'exit_stock_price': exit_point.get(f"s{self.pricing_criteria}", None),
                'exit_strategy_price': exit_strategy_price,
                'exit_volume': exit_point['v'],
                'exit_volume_weighted': exit_point['vw'],
                'exit_runs': exit_point['n'],
                'exit_stock_volume': exit_point.get('sv', None),
                'exit_stock_volume_weigthed': exit_point.get('svw', None),
                'stock_price_change_dollars': stock_price_change,
                'stock_price_change_percent': stock_price_change_percent,
                'contract_change_dollars': f'{contract_change_dollars:.2f}',
                'contract_change_percent': f'{contract_change_percent:.2f}',
                'strategy_profit_dollars': f'{strategy_profit_dollars:.2f}',
                'strategy_profit_percent': f'{strategy_profit_percent:.2f}'
            }

        simulation_data = []
        raw_data = self.merged_data if self.with_stock_prices else self.contract_data

        entry_start_time = datetime.strptime(f'{self.entry_date} {self.entry_exit_period[0]}',
                                             '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        entry_end_time = datetime.strptime(f'{self.entry_date} {self.entry_exit_period[1]}',
                                           '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        exit_start_time = datetime.strptime(f'{self.exit_date} {self.entry_exit_period[2]}',
                                            '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        exit_end_time = datetime.strptime(f'{self.exit_date} {self.entry_exit_period[3]}',
                                          '%Y-%m-%d %H:%M:%S').timestamp() * 1000

        entry_points = extract_points(raw_data, entry_start_time, entry_end_time)
        exit_points = extract_points(raw_data, exit_start_time, exit_end_time)

        for entry_point in entry_points:
            for exit_point in exit_points:
                simulated_trade = calculate_simulated_trade(entry_point, exit_point)
                simulation_data.append(simulated_trade)

        return pd.DataFrame(simulation_data) if simulation_data else None

    @staticmethod
    def get_meta_data(df: pd.DataFrame, includes_stock_price: bool = True) -> pd.DataFrame:
        meta_data = {
            'Average Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).mean(),
            'Average Strategy Profit (Dollars)': df['strategy_profit_dollars'].astype(float).mean(),
            'Standard Deviation of Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).std(),
            'Average Stock Price Change (Dollars)': df['stock_price_change_dollars'].astype(float).mean(),
            'Average Stock Price Change (Percent)': df['stock_price_change_percent'].astype(float).mean(),
            'Win Rate': (df['strategy_profit_dollars'].astype(float) > 0).mean(),
            'Average Contract Change (Dollars)': df['contract_change_dollars'].astype(float).mean(),
            'Average Contract Change (Percent)': df['contract_change_percent'].astype(float).mean(),
            'Standard Deviation of Contract Change (Percent)': df['contract_change_percent'].astype(float).std(),
            'Maximum Strategy Profit (Dollars)': df['strategy_profit_dollars'].astype(float).max(),
            'Minimum Strategy Profit (Dollars)': df['strategy_profit_dollars'].astype(float).min(),
            'Maximum Drawdown (Dollars)': df['strategy_profit_dollars'].astype(float).max() - df[
                'strategy_profit_dollars'].astype(float).min(),
            'Number of Trades': len(df),
            'Gap-Filled Trades': ((df['entry_runs'] == 0) | (df['exit_runs'] == 0)).sum(),
            'Profit Factor': df[df['strategy_profit_dollars'].astype(float) > 0]['strategy_profit_dollars'].astype(
                float).sum() / abs(
                df[df['strategy_profit_dollars'].astype(float) < 0]['strategy_profit_dollars'].astype(float).sum()),
            'Sharpe Ratio': df['strategy_profit_percent'].astype(float).mean() / df['strategy_profit_percent'].astype(
                float).std(),
            'Average Holding Period (Minutes)': ((pd.to_datetime(df['exit_time'], unit='ms') - pd.to_datetime(
                df['entry_time'], unit='ms')).dt.total_seconds() / 60).mean(),
        }

        return pd.DataFrame(meta_data.items(), columns=['Metric', 'Value'])


# test = SingleContractStrategy(ticker='nvda',
#                               strike=790,
#                               expiration_date='2024-03-01',
#                               quantity=1,
#                               entry_date='2024-02-28',
#                               is_call=True,
#                               exit_date='2024-02-28',
#                               strategy_type='long',
#                               entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
#                               timespan='minute',
#                               fill_gaps=True,
#                               with_stock_prices=True,
#                               per_contract_commission=0.01,
#                               multiplier=1,
#                               polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
#                               )
# # print(test.run_simulation().columns)
# print(SingleContractStrategy.get_meta_data(test.run_simulation()))
