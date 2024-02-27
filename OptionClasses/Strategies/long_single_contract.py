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

    def run_simulation(self) -> pd.DataFrame:
        pass


# test = LongSingleContractStrategy(ticker='aapl',
#                                   strike=180,
#                                   expiration_date='2024-03-01',
#                                   quantity=1,
#                                   entry_date='2024-02-22',
#                                   exit_date='2024-02-22',
#                                   entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
#                                   timespan='minute',
#                                   is_call=True,
#                                   fill_gaps=True,
#                                   per_contract_commission=0.01,
#                                   multiplier=1
#                                   )
#
# print(test.contract_data)