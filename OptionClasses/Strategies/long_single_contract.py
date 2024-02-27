from OptionClasses.Contracts.single_contract import SingleOptionsContract
import pandas as pd
from datetime import datetime, timedelta, time


class LongSingleContractStrategy:
    def __init__(self,
                 ticker: str,
                 strike: int or float,
                 expiration_date: str,
                 quantity: int,
                 entry_date: str,
                 exit_date: str,
                 is_call: bool,
                 entry_exit_period: tuple,
                 fill_gaps: bool = True,
                 timespan: str = 'minute',
                 per_contract_commission: float = 0.00,
                 closed_market_period: tuple = ('09:30:00', '16:00:00'),
                 pricing_criteria: str = 'h',
                 multiplier: int = 1,
                 polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                 ) -> None:

        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.is_call = is_call
        self.multiplier = multiplier
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period
        self.market_open, self.market_close = closed_market_period[0], closed_market_period[1]
        self.per_contract_commission = per_contract_commission
        self.quantity = quantity
        self.pricing_criteria = pricing_criteria

        contract = SingleOptionsContract(ticker=self.ticker, strike=self.strike, expiration_date=self.expiration_date,
                                         is_call=self.is_call)

        self.contract_data = contract.get_data(from_date=self.entry_date, to_date=self.exit_date,
                                               window_start_time=self.entry_exit_period[0],
                                               window_end_time=self.entry_exit_period[3],
                                               timespan=self.timespan, multiplier=self.multiplier,
                                               polygon_api_key=self.polygon_api_key)

        self.contract_data = self._fill_gaps() if fill_gaps else self.contract_data  # Checks if gaps should be filled

    def _fill_gaps(self) -> pd.DataFrame:
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

        for i in range(len(self.contract_data)):
            filled_data.append(list(self.contract_data.iloc[i]))  # Append as list instead of dict
            if i < (len(self.contract_data) - 1):
                current_time = datetime.fromtimestamp(self.contract_data.iloc[i]['t'] / 1000)
                next_time = datetime.fromtimestamp(self.contract_data.iloc[i + 1]['t'] / 1000)
                while current_time + interval < next_time and (
                        trading_start_time <= current_time.time() <= trading_end_time):
                    current_time += interval
                    filled_data.append([
                        self.contract_data.iloc[i]['v'],
                        self.contract_data.iloc[i]['vw'],
                        self.contract_data.iloc[i]['c'],  # assuming the open is equal to the previous close
                        self.contract_data.iloc[i]['c'],
                        self.contract_data.iloc[i]['c'],
                        self.contract_data.iloc[i]['c'],
                        int(current_time.timestamp() * 1000),
                        0  # fill gap indicator
                    ])

        return pd.DataFrame(filled_data, columns=self.contract_data.columns)

    def run_simulation(self):
        simulation_data = []
        entry_start_time = datetime.strptime(f'{self.entry_date} {self.entry_exit_period[0]}',
                                             '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        entry_end_time = datetime.strptime(f'{self.entry_date} {self.entry_exit_period[1]}',
                                           '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        exit_start_time = datetime.strptime(f'{self.exit_date} {self.entry_exit_period[2]}',
                                            '%Y-%m-%d %H:%M:%S').timestamp() * 1000
        exit_end_time = datetime.strptime(f'{self.exit_date} {self.entry_exit_period[3]}',
                                          '%Y-%m-%d %H:%M:%S').timestamp() * 1000

        entry_points = self.contract_data[
            (self.contract_data['t'] >= entry_start_time) & (self.contract_data['t'] <= entry_end_time)].to_dict(
            'records')
        exit_points = self.contract_data[
            (self.contract_data['t'] >= exit_start_time) & (self.contract_data['t'] <= exit_end_time)].to_dict(
            'records')

        for entry_point in entry_points:
            entry_time = entry_point['t']
            entry_contract_price = entry_point[self.pricing_criteria]  # CAN TINKER WITH AVERAGES HERE
            entry_strategy_price = entry_contract_price * self.quantity
            entry_volume = entry_point['v']
            entry_volume_weighted = entry_point['vw']
            entry_runs = entry_point['n']

            for exit_point in exit_points:
                exit_time = exit_point['t']
                exit_contract_price = exit_point[self.pricing_criteria]  # CAN TINKER WITH AVERAGES HERE
                exit_strategy_price = exit_contract_price * self.quantity
                exit_volume = exit_point['v']
                exit_volume_weighted = exit_point['vw']
                exit_runs = exit_point['n']

                contract_change_dollars = exit_contract_price - entry_contract_price
                contract_change_percent = contract_change_dollars / entry_contract_price
                commission_paid = self.quantity * self.per_contract_commission
                strategy_profit_dollars = exit_strategy_price - entry_strategy_price - (2 * commission_paid)
                strategy_profit_percent = strategy_profit_dollars / entry_strategy_price

                simulated_trade = {
                    'entry_time': entry_time,
                    'entry_contract_price': entry_contract_price,
                    'entry_strategy_price': entry_strategy_price,
                    'entry_volume': entry_volume,
                    'entry_volume_weighted': entry_volume_weighted,
                    'entry_runs': entry_runs,
                    'exit_time': exit_time,
                    'exit_contract_price': exit_contract_price,
                    'exit_strategy_price': exit_strategy_price,
                    'exit_volume': exit_volume,
                    'exit_volume_weighted': exit_volume_weighted,
                    'exit_runs': exit_runs,
                    'contract_change_dollars': f'{contract_change_dollars:.2f}',
                    'contract_change_percent': f'{contract_change_percent:.2f}',
                    'strategy_profit_dollars': f'{strategy_profit_dollars:.2f}',
                    'strategy_profit_percent': f'{strategy_profit_percent:.2f}'
                }

                simulation_data.append(simulated_trade)

        return pd.DataFrame(simulation_data)


test = LongSingleContractStrategy(ticker='aapl',
                                  strike=180,
                                  expiration_date='2024-03-01',
                                  quantity=1,
                                  entry_date='2024-02-22',
                                  exit_date='2024-02-22',
                                  entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
                                  timespan='minute',
                                  is_call=True,
                                  fill_gaps=True,
                                  per_contract_commission=0.01,
                                  multiplier=1
                                  )

print(test.run_simulation())