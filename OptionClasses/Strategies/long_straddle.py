from OptionClasses.Strategies.long_single_contract import LongSingleContractStrategy
import pandas as pd


class LongStraddleStrategy:
    def __init__(self,
                 ticker: str,
                 strike: int or float,
                 expiration_date: str,
                 quantity: int,
                 entry_date: str,
                 exit_date: str,
                 entry_exit_period: tuple,
                 fill_gaps: bool = True,
                 timespan: str = 'minute',
                 per_contract_commission: float = 0.00,
                 closed_market_period: tuple = ('09:30:00', '16:00:00'),
                 pricing_criteria: str = 'h',
                 multiplier: int = 1,
                 polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                 ) -> None:
        """
        Shared expiration, strike, ticker, and quantity in this class
        """
        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.multiplier = multiplier
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period
        self.market_open, self.market_close = closed_market_period[0], closed_market_period[1]
        self.per_contract_commission = per_contract_commission
        self.quantity = quantity
        self.pricing_criteria = pricing_criteria

        self.contract_1 = LongSingleContractStrategy(
            ticker=self.ticker,
            strike=self.strike,
            expiration_date=self.expiration_date,
            quantity=self.quantity,
            entry_date=self.entry_date,
            exit_date=self.exit_date,
            entry_exit_period=self.entry_exit_period,
            timespan=self.timespan,
            is_call=True,
            fill_gaps=fill_gaps,
            per_contract_commission=self.per_contract_commission,
            multiplier=self.multiplier,
            polygon_api_key=self.polygon_api_key
        )

        self.contract_2 = LongSingleContractStrategy(
            ticker=self.ticker,
            strike=self.strike,
            expiration_date=self.expiration_date,
            quantity=self.quantity,
            entry_date=self.entry_date,
            exit_date=self.exit_date,
            entry_exit_period=self.entry_exit_period,
            timespan=self.timespan,
            is_call=False,
            fill_gaps=fill_gaps,
            per_contract_commission=self.per_contract_commission,
            multiplier=self.multiplier,
            polygon_api_key=self.polygon_api_key
        )

    def run_simulation(self) -> pd.DataFrame:
        contract_1_trades = self.contract_1.run_simulation()
        contract_2_trades = self.contract_2.run_simulation()

        merged_df = pd.merge(contract_1_trades, contract_2_trades,
                             on=['entry_time', 'exit_time'])

        merged_df['combined_profit_dollars'] = pd.to_numeric(merged_df['strategy_profit_dollars_x']) + pd.to_numeric(
            merged_df[
                'strategy_profit_dollars_y'])
        merged_df['combined_profit_percent'] = pd.to_numeric(merged_df['strategy_profit_percent_x']) + pd.to_numeric(
            merged_df[
                'strategy_profit_percent_y'])
        merged_df['contract_change_dollars'] = pd.to_numeric(merged_df['contract_change_dollars_x']) + pd.to_numeric(
            merged_df[
                'contract_change_dollars_y'])
        merged_df['contract_change_percent'] = pd.to_numeric(merged_df['contract_change_percent_x']) + pd.to_numeric(
            merged_df[
                'contract_change_percent_y'])

        merged_df.drop(['strategy_profit_dollars_x', 'strategy_profit_dollars_y',
                        'strategy_profit_percent_x', 'strategy_profit_percent_y',
                        'contract_change_dollars_x', 'contract_change_dollars_y',
                        'contract_change_percent_x','contract_change_percent_y'], axis=1, inplace=True)

        merged_df.rename(columns={'ticker_x': 'ticker'}, inplace=True)

        return merged_df


    @staticmethod
    def get_meta_data(df: pd.DataFrame) -> pd.DataFrame:
        meta_data = {
            'Average Strategy Profit (Percent)': df['combined_profit_percent'].astype(float).mean(),
            'Average Strategy Profit (Dollars)': df['combined_profit_dollars'].astype(float).mean(),
            'Standard Deviation of Strategy Profit (Percent)': df['combined_profit_percent'].astype(float).std(),
            'Win Rate': (df['combined_profit_dollars'].astype(float) > 0).mean(),
            'Average Contract Change (Dollars)': df['contract_change_dollars'].astype(float).mean(),
            'Average Contract Change (Percent)': df['contract_change_percent'].astype(float).mean(),
            'Standard Deviation of Contract Change (Percent)': df['contract_change_percent'].astype(float).std(),
            'Maximum Strategy Profit (Dollars)': df['combined_profit_dollars'].astype(float).max(),
            'Minimum Strategy Profit (Dollars)': df['combined_profit_dollars'].astype(float).min(),
            'Maximum Drawdown (Dollars)': df['combined_profit_dollars'].astype(float).max() - df[
                'combined_profit_dollars'].astype(float).min(),
            'Number of Trades': len(df),
            'Gap-Filled Trades': ((df['entry_runs_x'] == 0) | (df['exit_runs_x'] == 0) |
                                  (df['entry_runs_y'] == 0) | (df['exit_runs_y'] == 0)).sum(),
            'Profit Factor': df[df['combined_profit_dollars'].astype(float) > 0]['combined_profit_dollars'].astype(
                float).sum() / abs(
                df[df['combined_profit_dollars'].astype(float) < 0]['combined_profit_dollars'].astype(float).sum()),
            'Sharpe Ratio': df['combined_profit_percent'].astype(float).mean() / df['combined_profit_percent'].astype(
                float).std(),
            'Average Holding Period (Minutes)': ((pd.to_datetime(df['exit_time'], unit='ms') - pd.to_datetime(
                df['entry_time'], unit='ms')).dt.total_seconds() / 60).mean(),
        }

        return pd.DataFrame(meta_data.items(), columns=['Metric', 'Value'])


test = LongStraddleStrategy(ticker='aapl',
                            strike=185,
                            expiration_date='2024-03-01',
                            quantity=1,
                            entry_date='2024-02-22',
                            exit_date='2024-02-22',
                            entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
                            timespan='minute',
                            fill_gaps=True,
                            per_contract_commission=0.01,
                            multiplier=1,
                            polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                            )
print(LongStraddleStrategy.get_meta_data(test.run_simulation()))