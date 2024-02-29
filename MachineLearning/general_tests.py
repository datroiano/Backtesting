import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from OptionClasses.Strategies.long_straddle import StraddleStrategy
from UseFunctions.date_time import from_unix_time, to_unix_time


def train_profit_predictor(data):
    # Convert entry_time and exit_time to seconds since midnight
    data['entry_seconds_since_midnight'] = pd.to_timedelta(data['entry_time']).dt.total_seconds()
    data['exit_seconds_since_midnight'] = pd.to_timedelta(data['exit_time']).dt.total_seconds()

    X = data[['entry_seconds_since_midnight', 'entry_volume_x',
              'entry_volume_weighted_x', 'entry_runs_x', 'exit_seconds_since_midnight',
              'exit_volume_x', 'exit_volume_weighted_x',
              'exit_runs_x', 'entry_volume_y', 'entry_volume_weighted_y',
              'entry_runs_y', 'exit_volume_y',
              'exit_volume_weighted_y']]
    y = data['strategy_profit_percent']

    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model


def predict_profit(model, entry_time, exit_time, entry_volume_x, entry_volume_weighted_x, entry_runs_x,
                   exit_volume_x, exit_volume_weighted_x, exit_runs_x, entry_volume_y, entry_volume_weighted_y,
                   entry_runs_y, exit_volume_y, exit_volume_weighted_y):
    entry_seconds = pd.to_timedelta(entry_time).total_seconds()
    exit_seconds = pd.to_timedelta(exit_time).total_seconds()

    data = pd.DataFrame({
        'entry_seconds_since_midnight': [entry_seconds],
        'entry_volume_x': [entry_volume_x],
        'entry_volume_weighted_x': [entry_volume_weighted_x],
        'entry_runs_x': [entry_runs_x],
        'exit_seconds_since_midnight': [exit_seconds],
        'exit_volume_x': [exit_volume_x],
        'exit_volume_weighted_x': [exit_volume_weighted_x],
        'exit_runs_x': [exit_runs_x],
        'entry_volume_y': [entry_volume_y],
        'entry_volume_weighted_y': [entry_volume_weighted_y],
        'entry_runs_y': [entry_runs_y],
        'exit_volume_y': [exit_volume_y],
        'exit_volume_weighted_y': [exit_volume_weighted_y]
    })

    return model.predict(data)[0]


trade_date = '2024-02-28'
# Train the profit predictor model
data = StraddleStrategy(ticker='nvda',
                        strike=790,
                        expiration_date='2024-03-01',
                        quantity=1,
                        entry_date=trade_date,
                        exit_date=trade_date,
                        strategy_type='short',
                        entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        ).run_simulation()

model = train_profit_predictor(data)

# Find rows where the right 8 characters of entry_time and exit_time match the input times
entry_time = '11:29:00'
exit_time = '15:59:00'
entry_volume_x = 30  # Example value for entry volume x
entry_volume_weighted_x = 5 # Example value for entry volume weighted x
entry_runs_x = 20  # Example value for entry runs x
exit_volume_x = 80  # Example value for exit volume x
exit_volume_weighted_x = 7  # Example value for exit volume weighted x
exit_runs_x = 4  # Example value for exit runs x
entry_volume_y = 12  # Example value for entry volume y
entry_volume_weighted_y = 20  # Example value for entry volume weighted y
entry_runs_y = 5  # Example value for entry runs y
exit_volume_y = 15  # Example value for exit volume y
exit_volume_weighted_y = 10  # Example value for exit volume weighted y

predicted_profit = predict_profit(model, entry_time=entry_time, exit_time=exit_time,
                                  entry_volume_x=entry_volume_x,
                                  entry_volume_weighted_x=entry_volume_weighted_x,
                                  entry_runs_x=entry_runs_x,
                                  exit_volume_x=exit_volume_x,
                                  exit_volume_weighted_x=exit_volume_weighted_x,
                                  exit_runs_x=exit_runs_x,
                                  entry_volume_y=entry_volume_y,
                                  entry_volume_weighted_y=entry_volume_weighted_y,
                                  entry_runs_y=entry_runs_y,
                                  exit_volume_y=exit_volume_y,
                                  exit_volume_weighted_y=exit_volume_weighted_y)


result = data[(data['entry_time'] == to_unix_time(f'{trade_date} {entry_time}')) & (data['exit_time'] == to_unix_time(f'{trade_date} {exit_time}'))]


print(f"Predicted Profit (%): {predicted_profit * 100:.4f}")
print("Real Data:")
for index, row in result.iterrows():
    print(row)
