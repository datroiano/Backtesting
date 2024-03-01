import pandas as pd
from OptionClasses.Strategies.straddle import StraddleStrategy
from UseFunctions.date_time import to_unix_time
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.model_selection import train_test_split
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# WORK IN PROGRESS (NOT WORKING)

def apply_neural_network(data):
    # Split data into features and target
    x = data.drop(columns=['strategy_profit_percent'])
    y = data['strategy_profit_percent']

    # Convert DataFrame to numpy arrays
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=42)
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    # Convert numpy arrays to PyTorch tensors
    x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    # Create PyTorch dataset and dataloaders
    train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=False)

    # Define the neural network architecture
    model = nn.Sequential(
        nn.Linear(x_train.shape[1], 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1)
    )

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    # Train the model
    num_epochs = 50
    for epoch in range(num_epochs):
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs.squeeze(), targets)
            loss.backward()
            optimizer.step()

    # Evaluate the model
    with torch.no_grad():
        outputs = model(x_test_tensor)
        mse = criterion(outputs.squeeze(), y_test_tensor).item()

    return mse, model, list(x.columns)


def predict_profit_percent_specific_inputs(model, feature_names, **kwargs):
    # Convert input features to PyTorch tensor
    data = torch.tensor([[kwargs[feature] for feature in feature_names]], dtype=torch.float32)

    # Make prediction using the model
    with torch.no_grad():
        prediction = model(data)

    return prediction.item()  # Return the predicted profit percent


def print_profit_percent_for_times(df, entry_time, exit_time):
    filtered_df = df[(df['entry_time'] == entry_time) & (df['exit_time'] == exit_time)]
    if not filtered_df.empty:
        print(f"Actual Profit Percent: {filtered_df['strategy_profit_percent'].values[0] * 100:.4f} %")
    else:
        print("No data found for Entry Time:", entry_time, "and Exit Time:", exit_time)


# Example usage
test = StraddleStrategy(ticker='aapl',
                        strike=185,
                        expiration_date='2024-03-01',
                        quantity=1,
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


model = apply_neural_network(test)


entry_time = to_unix_time('2024-02-28 11:28:00')
exit_time = to_unix_time('2024-02-28 15:30:00')
entry_stock_price = 180
exit_stock_price = 175

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
