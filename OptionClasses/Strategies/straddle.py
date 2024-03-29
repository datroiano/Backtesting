from OptionClasses.Strategies.single_contract import SingleContractStrategy
import pandas as pd
from UseFunctions.print_df_excel import save_df_to_excel
from UseFunctions.date_time import unix_ms_to_seconds_since_midnight


class StraddleStrategy:
    def __init__(self,
                 ticker: str, strike: int or float, expiration_date: str, quantity: int, entry_date: str,
                 exit_date: str, entry_exit_period: tuple, strategy_type: str = 'long', fill_gaps: bool = True,
                 timespan: str = 'minute', per_contract_commission: float = 0.00,
                 closed_market_period: tuple = ('09:30:00', '16:00:00'), pricing_criteria: str = 'h',
                 multiplier: int = 1, polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz') -> None:
        """
        Shared expiration, strike, ticker, and quantity in this class
        Can be either short or long
        for_machine_learning: intended to clean data specifically for linear-model relationships (abs, for instance)
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

    def run_simulation(self) -> pd.DataFrame or None:
        contract_1_trades = self.contract_1.run_simulation()
        contract_2_trades = self.contract_2.run_simulation()
        try:
            merged_df = pd.merge(contract_1_trades, contract_2_trades, on=['entry_time', 'exit_time'])
        except TypeError:
            return None
        is_long = self.strategy_type == 'LONG'

        # Appending metadata (for now, strike is all we need)
        merged_df['strike_price'] = self.strike

        # Dealing with strategic profit (cleaning)
        one_way_commission = self.quantity * self.per_contract_commission
        contract_change = pd.to_numeric(merged_df['exit_contract_price_x']) + pd.to_numeric(
            merged_df['exit_contract_price_y']) - pd.to_numeric(merged_df['entry_contract_price_x']) - pd.to_numeric(
            merged_df['entry_contract_price_y'])

        dollars_profit = (contract_change if is_long else -contract_change) - (one_way_commission * 2)
        entry_value_less_commission = pd.to_numeric(merged_df['entry_contract_price_x']) + pd.to_numeric(
            merged_df['entry_contract_price_y'])
        merged_df.drop(['exit_contract_price_x', 'exit_contract_price_y', 'entry_contract_price_x',
                        'entry_contract_price_y'], axis=1, inplace=True)
        merged_df['strategy_profit_dollars'] = dollars_profit
        merged_df['strategy_profit_percent'] = dollars_profit / (entry_value_less_commission -
                                                                 one_way_commission * 2 + 1e-8)  # Avoids ZeroDivision
        merged_df['contract_change_dollars'] = contract_change
        merged_df['contract_change_percent'] = contract_change / (
                entry_value_less_commission + 1e-8)  # Add a small value to avoid division by zero

        # Combining and cleaning volume
        merged_df['entry_volume'] = merged_df['entry_volume_x'] + merged_df['entry_volume_y']
        merged_df['exit_volume'] = merged_df['exit_volume_x'] + merged_df['exit_volume_y']
        merged_df.drop(['entry_volume_x', 'entry_volume_y', 'exit_volume_x', 'exit_volume_y'], axis=1, inplace=True)

        # Combining and cleaning volume weighted average price
        merged_df['entry_volume_weighted'] = merged_df['entry_volume_weighted_x'] + merged_df['entry_volume_weighted_y']
        merged_df['exit_volume_weighted'] = merged_df['exit_volume_weighted_x'] + merged_df['exit_volume_weighted_y']
        merged_df.drop(['entry_volume_weighted_x', 'entry_volume_weighted_y', 'exit_volume_weighted_x',
                        'exit_volume_weighted_y'], axis=1, inplace=True)

        # Combining transactions during period (still options)
        merged_df['entry_transactions'] = merged_df['entry_runs_x'] + merged_df['entry_runs_y']
        merged_df['exit_transactions'] = merged_df['exit_runs_x'] + merged_df['exit_runs_y']
        merged_df.drop(['entry_runs_x', 'entry_runs_y', 'exit_runs_x', 'exit_runs_y'], axis=1, inplace=True)

        # Combining and cleaning stock prices
        merged_df['entry_stock_price'] = merged_df['entry_stock_price_x']
        merged_df['exit_stock_price'] = merged_df['exit_stock_price_x']
        merged_df.drop(['entry_stock_price_x', 'entry_stock_price_y', 'exit_stock_price_x', 'exit_stock_price_y'],
                       axis=1, inplace=True)

        # Combining and cleaning stock volumes
        merged_df['entry_stock_volume'] = merged_df['entry_stock_volume_x']
        merged_df['exit_stock_volume'] = merged_df['exit_stock_volume_x']
        merged_df.drop(['entry_stock_volume_x', 'entry_stock_volume_y', 'exit_stock_volume_x', 'exit_stock_volume_y'],
                       axis=1, inplace=True)

        # Combining and cleaning stock volume weighted average price
        merged_df['entry_stock_volume_weighted'] = merged_df['entry_stock_volume_weighted_x']
        merged_df['exit_stock_volume_weighted'] = merged_df['exit_stock_volume_weighted_x']
        merged_df.drop(['entry_stock_volume_weighted_x', 'entry_stock_volume_weighted_y',
                        'exit_stock_volume_weighted_x', 'exit_stock_volume_weighted_y'],
                       axis=1, inplace=True)

        # Combining and cleaning stock price change dollars
        merged_df['stock_price_change_dollars'] = merged_df['stock_price_change_dollars_x']
        merged_df['stock_price_change_percent'] = merged_df['stock_price_change_percent_x']
        merged_df.drop(['stock_price_change_dollars_x', 'stock_price_change_dollars_y',
                        'stock_price_change_percent_x', 'stock_price_change_percent_y'], axis=1, inplace=True)
        # Drop redundant or unnecessary columns
        merged_df.drop(['exit_strategy_price_x', 'contract_change_dollars_x', 'contract_change_percent_x',
                        'strategy_profit_dollars_x', 'strategy_profit_percent_x', 'entry_strategy_price_y',
                        'exit_strategy_price_y', 'contract_change_dollars_y', 'contract_change_percent_y',
                        'strategy_profit_dollars_y', 'strategy_profit_percent_y', 'entry_strategy_price_x'],
                       axis=1, inplace=True)

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
            # 'Gap-Filled Trades': pass,
            'Profit Factor': df[df['strategy_profit_dollars'].astype(float) > 0]['strategy_profit_dollars'].astype(
                float).sum() / abs(
                df[df['strategy_profit_dollars'].astype(float) < 0]['strategy_profit_dollars'].astype(float).sum()),
            'Sharpe Ratio': df['strategy_profit_percent'].astype(float).mean() / df['strategy_profit_percent'].astype(
                float).std(),
            'Average Holding Period (Minutes)': ((pd.to_datetime(df['exit_time'], unit='ms') - pd.to_datetime(
                df['entry_time'], unit='ms')).dt.total_seconds() / 60).mean(),
        }

        return pd.DataFrame(meta_data.items(), columns=['Metric', 'Value'])

    @staticmethod
    def get_meta_data_not_dollars(df: pd.DataFrame) -> pd.DataFrame:
        meta_data = {
            'Average Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).mean(),
            'Standard Deviation of Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).std(),
            'Win Rate': (df['strategy_profit_percent'].astype(float) > 0).mean(),
            'Maximum Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).max(),
            'Minimum Strategy Profit (Percent)': df['strategy_profit_percent'].astype(float).min(),
            'Sharpe Ratio': df['strategy_profit_percent'].astype(float).mean() / df['strategy_profit_percent'].astype(
                float).std(),
        }

        return pd.DataFrame(meta_data.items(), columns=['Metric', 'Value'])

    @staticmethod
    def find_entry_exit_data(data: pd.DataFrame, entry_time: str or int, exit_time: str or int) -> dict or None:
        filtered_data = data[(data['entry_time'] == entry_time) & (data['exit_time'] == exit_time)]
        if filtered_data.empty:
            return None
        entry_exit_dict = filtered_data.iloc[0].to_dict()
        return entry_exit_dict

