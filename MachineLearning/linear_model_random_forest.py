import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from OptionClasses.Strategies.straddle import StraddleStrategy
from UseFunctions.date_time import to_unix_time, readable_time_to_seconds_since_midnight
from UseFunctions.print_df_excel import print_row_values


# BEST MODEL SO FAR


def apply_predictive_model(df: pd.DataFrame):
    x = df.drop(columns=['strategy_profit_dollars', 'strategy_profit_percent', 'contract_change_dollars',
                         'contract_change_percent', 'entry_stock_price', 'exit_stock_price',
                         'stock_price_change_dollars'])
    y = df['strategy_profit_percent']
    feature_names = x.columns
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=42)
    model = RandomForestRegressor(random_state=42)  # Using Random Forest Regression
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return mse, model, feature_names


test1 = StraddleStrategy(ticker='aapl',
                         strike=180,
                         expiration_date='2024-03-01',
                         quantity=5,
                         entry_date='2024-02-28',
                         exit_date='2024-02-28',
                         strategy_type='long',
                         entry_exit_period=('10:30:00', '11:30:00', '14:30:00', '16:00:00'),
                         timespan='minute',
                         fill_gaps=True,
                         per_contract_commission=0.01,
                         multiplier=1,
                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                         ).run_simulation()

test2 = StraddleStrategy(ticker='nvda',
                         strike=790,
                         expiration_date='2024-03-01',
                         quantity=5,
                         entry_date='2024-02-26',
                         exit_date='2024-02-26',
                         strategy_type='long',
                         entry_exit_period=('10:30:00', '11:30:00', '14:30:00', '16:00:00'),
                         timespan='minute',
                         fill_gaps=True,
                         per_contract_commission=0.01,
                         multiplier=1,
                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                         ).run_simulation()

test3 = StraddleStrategy(ticker='adbe',
                         strike=565,
                         expiration_date='2024-03-01',
                         quantity=5,
                         entry_date='2024-02-27',
                         exit_date='2024-02-27',
                         strategy_type='long',
                         entry_exit_period=('10:30:00', '11:30:00', '14:30:00', '16:00:00'),
                         timespan='minute',
                         fill_gaps=True,
                         per_contract_commission=0.01,
                         multiplier=1,
                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                         ).run_simulation()

test4 = StraddleStrategy(ticker='aapl',
                         strike=185,
                         expiration_date='2024-03-08',
                         quantity=5,
                         entry_date='2024-02-26',
                         exit_date='2024-02-26',
                         strategy_type='long',
                         entry_exit_period=('10:30:00', '11:30:00', '14:30:00', '16:00:00'),
                         timespan='minute',
                         fill_gaps=True,
                         per_contract_commission=0.01,
                         multiplier=1,
                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                         ).run_simulation()

full_set = pd.concat([test4])
model_from_test = apply_predictive_model(full_set)


def predict_profit_percent_specific_inputs(model, feature_names, **kwargs):
    data = pd.DataFrame([kwargs])
    data = data[feature_names]
    prediction = model.predict(data)
    return prediction[0]  # Return the predicted profit percent


test4_exception = StraddleStrategy(ticker='aapl',
                                   strike=180,
                                   expiration_date='2024-03-08',
                                   quantity=5,
                                   entry_date='2024-02-26',
                                   exit_date='2024-02-26',
                                   strategy_type='long',
                                   entry_exit_period=('10:30:00', '11:30:00', '14:30:00', '16:00:00'),
                                   timespan='minute',
                                   fill_gaps=True,
                                   per_contract_commission=0.01,
                                   multiplier=1,
                                   polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz',
                                   for_machine_learning=False
                                   ).run_simulation()

x1 = print_row_values(test4_exception, entry_time=to_unix_time('2024-02-26 10:45:00'),
                 exit_time=to_unix_time('2024-02-26 14:45:00'))

# GUESS CRITERIA
entry_time = readable_time_to_seconds_since_midnight('10:45:00')
exit_time = readable_time_to_seconds_since_midnight('14:45:00')
entry_volume = 83.0
exit_volume = entry_volume
entry_volume_weighted = 5.5943000000000005
exit_volume_weighted = entry_volume_weighted
entry_transactions = 10
exit_transactions = 15
entry_stock_price = 181
exit_stock_price = 181.5
entry_stock_volume = 90000
exit_stock_volume = entry_stock_volume
entry_stock_volume_weighted = entry_stock_price
exit_stock_volume_weighted = exit_stock_price
stock_price_change_percent = abs((exit_stock_price - entry_stock_price) / entry_stock_price)

predicted_profit = predict_profit_percent_specific_inputs(
    model=model_from_test[1],  # Passing the model
    feature_names=model_from_test[2],  # Passing the feature names
    entry_time=entry_time,
    exit_time=exit_time,
    entry_volume=entry_volume,
    exit_volume=exit_volume,
    entry_volume_weighted=entry_volume_weighted,
    exit_volume_weighted=exit_volume_weighted,
    entry_transactions=entry_transactions,
    exit_transactions=exit_transactions,
    entry_stock_price=entry_stock_price,
    exit_stock_price=exit_stock_price,
    entry_stock_volume=entry_stock_volume,
    exit_stock_volume=exit_stock_volume,
    entry_stock_volume_weighted=entry_stock_volume_weighted,
    exit_stock_volume_weighted=exit_stock_volume_weighted,
    stock_price_change_percent=stock_price_change_percent
)

print(f"\nPredicted Profit Percent: {predicted_profit * 100:.4f}%")
print(f"Actual Returned Profit: {x1[0] * 100:.4f}%")
