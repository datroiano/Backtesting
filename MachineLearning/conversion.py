import pandas as pd
from UseFunctions.date_time import unix_ms_to_seconds_since_midnight


def clean_df(df: pd.DataFrame, midnight_time: bool = True) -> pd.DataFrame:
    if midnight_time:
        df['entry_time'] = df['entry_time'].apply(unix_ms_to_seconds_since_midnight)
        df['exit_time'] = df['exit_time'].apply(unix_ms_to_seconds_since_midnight)

    df.drop(['exit_stock_volume_weighted', 'entry_stock_volume_weighted',
             'entry_volume_weighted', 'exit_volume_weighted'], axis=1, inplace=True)

    stock_price_difference = abs(df['exit_stock_price'] / df['entry_stock_price']) - 1
    df['stock_linear_correlated_measure'] = stock_price_difference
    df.drop(['entry_stock_price', 'exit_stock_price', 'strike_price'], axis=1, inplace=True)

    # Get rid of other "dependent" variables
    df.drop(['contract_change_dollars', 'strategy_profit_dollars', 'contract_change_percent',
             'stock_price_change_dollars', 'stock_price_change_percent'], axis=1, inplace=True)

    # Change other measures to deltas, rather than having absolute numbers
    df['delta_volume_percent'] = (df['exit_volume'] / df['entry_volume']) - 1
    df.drop(['exit_volume', 'entry_volume'], axis=1, inplace=True)
    df['delta_stock_volume_percent'] = (df['exit_stock_volume'] / df['entry_stock_volume']) - 1
    df.drop(['exit_stock_volume', 'entry_stock_volume'], axis=1, inplace=True)
    df['delta_transactions_percent'] = (df['exit_transactions'] / df['entry_transactions']) - 1
    df.drop(['exit_transactions', 'entry_transactions'], axis=1, inplace=True)

    return df



