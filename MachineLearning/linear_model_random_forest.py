import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from OptionClasses.Strategies.straddle import StraddleStrategy
from UseFunctions.date_time import to_unix_time


# BEST MODEL SO FAR


def apply_predictive_model(df: pd.DataFrame):
    x = df.drop(columns=['strategy_profit_dollars', 'strategy_profit_percent', 'contract_change_dollars',
                         'contract_change_percent', 'entry_stock_price', 'exit_stock_price'])
    y = df['strategy_profit_percent']
    feature_names = x.columns
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=42)
    model = RandomForestRegressor(random_state=42)  # Using Random Forest Regression
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return mse, model, feature_names


test1 = StraddleStrategy(ticker='aapl',
                         strike=185,
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

full_set = pd.concat([test1, test2, test3, test4])
model = apply_predictive_model(full_set)


def predict_profit_percent_specific_inputs(model, feature_names, **kwargs):
    data = pd.DataFrame([kwargs])
    data = data[feature_names]
    prediction = model.predict(data)
    return prediction[0]  # Return the predicted profit percent
