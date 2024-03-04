import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# BEST MODEL SO FAR


def generate_predictive_model(df: pd.DataFrame):
    x = df.drop(columns=['strategy_profit_percent'])
    y = df['strategy_profit_percent']
    feature_names = x.columns
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(random_state=42)  # Using Random Forest Regression
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return mse, model, feature_names


