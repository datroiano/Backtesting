import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from OptionClasses.Strategies.straddle import StraddleStrategy
from UseFunctions.date_time import to_unix_time

# BEST MODEL SO FAR


def apply_predictive_model(data):
    x = data.drop(columns=['strategy_profit_percent'])
    y = data['strategy_profit_percent']
    feature_names = x.columns  # Get feature names
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(random_state=42)  # Using Random Forest Regressor
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return mse, model, feature_names


test = StraddleStrategy(ticker='nvda',
                        strike=790,
                        expiration_date='2024-03-01',
                        quantity=5,
                        entry_date='2024-02-28',
                        exit_date='2024-02-28',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        ).run_simulation()

model = apply_predictive_model(test)


def predict_profit_percent_specific_inputs(model, feature_names, **kwargs):
    data = pd.DataFrame([kwargs])
    data = data[feature_names]
    prediction = model.predict(data)
    return prediction[0]  # Return the predicted profit percent


def print_profit_percent_for_times(df, entry_time, exit_time):
    filtered_df = df[(df['entry_time'] == entry_time) & (df['exit_time'] == exit_time)]
    if not filtered_df.empty:
        print(f"Actual Profit Percent: {filtered_df['strategy_profit_percent'].values[0] * 100:.4f} %")
    else:
        print("No data found for Entry Time:", entry_time, "and Exit Time:", exit_time)


entry_time = to_unix_time('2024-02-28 11:28:00')
exit_time = to_unix_time('2024-02-28 15:30:00')
entry_stock_price = 790
exit_stock_price = 800

predicted_profit = predict_profit_percent_specific_inputs(
    model[1], model[2],
    entry_time=entry_time,
    entry_volume_x=240,
    entry_volume_weighted_x=0.2,
    entry_runs_x=50,
    exit_time=exit_time,
    exit_volume_x=240,
    exit_volume_weighted_x=0.2,
    exit_runs_x=15,
    entry_volume_y=10,
    entry_volume_weighted_y=4,
    entry_runs_y=4,
    exit_volume_y=50,
    exit_volume_weighted_y=4,
    exit_runs_y=10,
    entry_stock_price=entry_stock_price,
    entry_stock_volume=180000,
    exit_stock_price=exit_stock_price,
    exit_stock_volume=180000,
    stock_price_change_percent=abs((exit_stock_price / entry_stock_price) - 1)
)
print_profit_percent_for_times(test, entry_time, exit_time)
print(f"Predicted Profit Percent: {predicted_profit * 100:.4f} %")