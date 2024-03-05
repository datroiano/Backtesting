from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from MachineLearning.linear_model_random_forest import generate_predictive_model
from TestCases.straddle_runner import learning_frame
from UseFunctions.date_time import readable_time_to_seconds_since_midnight
from UseFunctions.entries import calculate_stock_linear_correlated_measure


def guess_profit_percent(model: RandomForestRegressor, feature_names: list, **kwargs):
    """
    Guess the dependent variable 'strategy_profit_percent' based on input values for independent features.

    Parameters:
    - model: Trained RandomForestRegressor model
    - feature_names: List of feature names used in the model
    - **kwargs: Keyword arguments containing input values for independent features to be guessed upon

    Returns:
    - Predicted strategy_profit_percent based on parameters entered
    """
    # Create a dataframe with input values
    input_df = pd.DataFrame([kwargs], columns=feature_names)
    # Predict strategy_profit_percent using the model
    prediction = model.predict(input_df)
    return prediction[0]


mse, model, feature_names = generate_predictive_model(learning_frame)

# GUESS PARAMETERS
entry_time = readable_time_to_seconds_since_midnight('10:30:00')
exit_time = readable_time_to_seconds_since_midnight('14:30:00')
exit_stock_price = 180
entry_stock_price = 180
strike_price = 180

# Guess the strategy_profit_percent
predicted_profit_percent = guess_profit_percent(
    model,
    feature_names,
    entry_time=entry_time,
    exit_time=exit_time,
    stock_linear_correlated_measure=calculate_stock_linear_correlated_measure(
        exit_stock_price=exit_stock_price,
        entry_stock_price=entry_stock_price,
        strike_price=strike_price),
    delta_volume_percent=0,
    delta_stock_volume_percent=0,
    delta_transactions_percent=0)

print("Predicted strategy_profit_percent:", predicted_profit_percent)

filtered_df = learning_frame[(learning_frame['entry_time'] == entry_time) & (learning_frame['exit_time'] == exit_time)]

# Print the strategy_profit_percent column
if not filtered_df.empty:
    print('Actual Profit:', filtered_df['strategy_profit_percent'])
else:
    print("No matching entry and exit times found in learning_frame.")
