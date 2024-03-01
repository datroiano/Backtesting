from OptionClasses.Strategies.single_contract import SingleContractStrategy
import pandas as pd


class StraddleStrategy:
    def __init__(self,
                 ticker: str,
                 strike: int or float,
                 expiration_date: str,
                 quantity: int,
                 entry_date: str,
                 exit_date: str,
                 entry_exit_period: tuple,
                 strategy_type: str = 'long',
                 fill_gaps: bool = True,
                 timespan: str = 'minute',
                 per_contract_commission: float = 0.00,
                 closed_market_period: tuple = ('09:30:00', '16:00:00'),
                 pricing_criteria: str = 'h',
                 multiplier: int = 1,
                 polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz',
                 for_machine_learning: bool = True
                 ) -> None:
        """
        Shared expiration, strike, ticker, and quantity in this class
        Can be either short or long
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
        self.strategy_type = strategy_type.upper()
        self.for_machine_learning = for_machine_learning

        self.contract_1 = SingleContractStrategy(
            ticker=self.ticker,
            strike=self.strike,
            expiration_date=self.expiration_date,
            quantity=self.quantity,
            entry_date=self.entry_date,
            exit_date=self.exit_date,
            entry_exit_period=self.entry_exit_period,
            timespan=self.timespan,
            strategy_type=self.strategy_type,
            is_call=True,
            fill_gaps=fill_gaps,
            per_contract_commission=self.per_contract_commission,
            multiplier=self.multiplier,
            polygon_api_key=self.polygon_api_key,
            with_stock_prices=True
        )

        self.contract_2 = SingleContractStrategy(
            ticker=self.ticker,
            strike=self.strike,
            expiration_date=self.expiration_date,
            quantity=self.quantity,
            entry_date=self.entry_date,
            exit_date=self.exit_date,
            entry_exit_period=self.entry_exit_period,
            timespan=self.timespan,
            strategy_type=self.strategy_type,
            is_call=False,
            fill_gaps=fill_gaps,
            per_contract_commission=self.per_contract_commission,
            multiplier=self.multiplier,
            polygon_api_key=self.polygon_api_key,
            with_stock_prices=True
        )

    def run_simulation(self) -> pd.DataFrame:
        contract_1_trades = self.contract_1.run_simulation()
        contract_2_trades = self.contract_2.run_simulation()

        merged_df = pd.merge(contract_1_trades, contract_2_trades, on=['entry_time', 'exit_time'])

        is_long = self.strategy_type == 'LONG'

        one_way_commission = self.quantity * self.per_contract_commission
        contract_change = (pd.to_numeric(merged_df['exit_contract_price_x']) + pd.to_numeric(
            merged_df['exit_contract_price_y']) -
                           pd.to_numeric(merged_df['entry_contract_price_x']) - pd.to_numeric(
                    merged_df['entry_contract_price_y']))
        dollars_profit = (contract_change if is_long else -contract_change) - (one_way_commission * 2)
        entry_value_less_commission = (pd.to_numeric(merged_df['entry_contract_price_x']) + pd.to_numeric(
            merged_df['entry_contract_price_y']))

        merged_df['entry_stock_price'] = merged_df['entry_stock_price_x']
        merged_df['entry_strike_less_stock'] = self.strike - merged_df['entry_stock_price_x']
        merged_df['entry_stock_volume'] = merged_df['entry_stock_volume_x']
        merged_df['exit_stock_price'] = merged_df['exit_stock_price_x']
        merged_df['exit_strike_less_stock'] = self.strike - merged_df['exit_stock_price_x']
        merged_df['exit_stock_volume'] = merged_df['exit_stock_volume_x']
        merged_df['stock_price_change_dollars'] = merged_df['stock_price_change_dollars_x']
        merged_df['stock_price_change_percent'] = merged_df['stock_price_change_percent_x']

        merged_df['strategy_profit_dollars'] = dollars_profit
        merged_df['strategy_profit_percent'] = abs(dollars_profit / (
                    entry_value_less_commission - one_way_commission * 2 + 1e-8)) if self.for_machine_learning else dollars_profit / (
                    entry_value_less_commission - one_way_commission * 2 + 1e-8)  # Avoids ZeroDivision
        merged_df['contract_change_dollars'] = contract_change
        merged_df['contract_change_percent'] = contract_change / (
                    entry_value_less_commission + 1e-8)  # Add a small value to avoid division by zero

        merged_df.drop(['exit_contract_price_x', 'exit_contract_price_y', 'entry_contract_price_x',
                        'entry_contract_price_y', 'entry_stock_price_x', 'entry_stock_price_y',
                        'entry_stock_volume_weighted_x', 'entry_stock_volume_weighted_y',
                        'exit_stock_volume_weigthed_x', 'entry_strategy_price_x', 'exit_strategy_price_x',
                        'contract_change_dollars_x', 'contract_change_percent_x', 'strategy_profit_dollars_x',
                        'strategy_profit_percent_x', 'entry_strategy_price_y', 'exit_strategy_price_y',
                        'contract_change_dollars_y', 'contract_change_percent_y', 'strategy_profit_dollars_y',
                        'strategy_profit_percent_y', 'stock_price_change_dollars', 'exit_stock_price',
                        'stock_price_change_dollars_x', 'stock_price_change_percent_x', 'exit_stock_volume_weigthed_y',
                        'stock_price_change_dollars_y', 'stock_price_change_percent_y', 'entry_stock_price',
                        'entry_stock_volume_x', 'entry_stock_volume_y',  'exit_stock_price_x', 'exit_stock_price_y',
                        'exit_stock_volume_x', 'exit_stock_volume_y'], axis=1, inplace=True)

        merged_df.rename(columns={'ticker_x': 'ticker'}, inplace=True)

        return merged_df

    @staticmethod
    def get_meta_data(df: pd.DataFrame) -> pd.DataFrame:
        meta_data = {
            'Average Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).mean(),
            'Average Strategy Profit (Dollars)': df['strategy_profit_dollars'].astype(float).mean(),
            'Standard Deviation of Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).std(),
            'Win Rate': (df['strategy_profit_dollars'].astype(float) > 0).mean(),
            'Average Contract Change (Dollars)': df['contract_change_dollars'].astype(float).mean(),
            'Average Contract Change (Percent)': df['contract_change_percent'].astype(float).mean(),
            'Standard Deviation of Contract Change (Percent)': df['contract_change_percent'].astype(float).std(),
            'Maximum Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).max(),
            'Minimum Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).min(),
            'Maximum Drawdown (Dollars)': df['strategy_profit_dollars'].astype(float).max() - df[
                'strategy_profit_dollars'].astype(float).min(),
            'Number of Trades': len(df),
            'Gap-Filled Trades': ((df['entry_runs_x'] == 0) | (df['exit_runs_x'] == 0) |
                                  (df['entry_runs_y'] == 0) | (df['exit_runs_y'] == 0)).sum(),
            'Profit Factor': df[df['strategy_profit_dollars'].astype(float) > 0]['strategy_profit_dollars'].astype(
                float).sum() / abs(
                df[df['strategy_profit_dollars'].astype(float) < 0]['strategy_profit_dollars'].astype(float).sum()),
            'Sharpe Ratio': df['strategy_profit_percent'].astype(float).mean() / df['strategy_profit_percent'].astype(
                float).std(),
            'Average Holding Period (Minutes)': ((pd.to_datetime(df['exit_time'], unit='ms') - pd.to_datetime(
                df['entry_time'], unit='ms')).dt.total_seconds() / 60).mean(),
        }

        return pd.DataFrame(meta_data.items(), columns=['Metric', 'Value'])

#
# test = StraddleStrategy(ticker='aapl',
#                         strike=180,
#                         expiration_date='2024-03-01',
#                         quantity=1,
#                         entry_date='2024-02-28',
#                         exit_date='2024-02-28',
#                         strategy_type='long',
#                         entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
#                         timespan='minute',
#                         fill_gaps=True,
#                         per_contract_commission=0.01,
#                         multiplier=1,
#                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
#                         )


# print(test.run_simulation().columns)
# print(StraddleStrategy.get_meta_data(test.run_simulation()))
# print(make_df_input(test.run_simulation()))
