def create_options_ticker(ticker: str, strike: float, expiration_date: str, contract_type: bool) -> str:
    """
    Strike formatting will look like this:
    1000: 01000000
    1000.5: 01000500
    170.5: 00170500
    """
    ticker = str(ticker.upper())
    strike = str(float(strike))
    expiration_year = expiration_date[2:4]
    expiration_month = expiration_date[5:7]
    expiration_day = expiration_date[8:]
    contract_type = 'C' if contract_type else 'P'

    decimal_find = strike.find('.', )
    num_dec = len(strike) - decimal_find - 1
    strike = strike.replace(".", "")

    strike_mapping = {1: {
        1: f'00000{strike}00',
        2: f'0000{strike}00',
        3: f'000{strike}00',
        4: f'00{strike}00',
        5: f'0{strike}00',
        6: f'{strike}00',
    }, 2: {
        1: f'000000{strike}0',
        2: f'00000{strike}0',
        3: f'0000{strike}0',
        4: f'000{strike}0',
        5: f'0{strike}0',
        6: f'{strike}00',
        7: f'{strike}0'
    }
    }

    strike_string_for_insertion = strike_mapping.get(num_dec, '')[len(strike)]

    expiration_month = f'0{expiration_month}' if len(expiration_month) == 1 else expiration_month
    expiration_year = f'0{expiration_year}' if len(expiration_year) == 1 else expiration_year
    expiration_day = f'0{expiration_day}' if len(expiration_day) == 1 else expiration_day

    expiry = f'{expiration_year}{expiration_month}{expiration_day}'

    return f'O:{ticker}{expiry}{contract_type}{strike_string_for_insertion}'


def calculate_stock_linear_correlated_measure(exit_stock_price, entry_stock_price, strike_price):
    """
    Calculate the stock_linear_correlated_measure based on exit_stock_price, entry_stock_price, and strike_price.

    Parameters:
    - exit_stock_price: Exit stock price
    - entry_stock_price: Entry stock price
    - strike_price: Strike price at entry

    Returns:
    - Stock_linear_correlated_measure
    """
    # Calculate the difference between the exit stock price and entry stock price
    stock_price_difference = abs(exit_stock_price - entry_stock_price)

    # Calculate the difference between the exit stock price and strike price at entry
    stock_strike_difference = abs(exit_stock_price - strike_price)

    # Use the maximum of stock_strike_difference and entry_stock_price to ensure capturing the steeper movement
    divisor = max(stock_strike_difference, entry_stock_price)

    # Calculate the stock_linear_correlated_measure
    stock_linear_correlated_measure = stock_price_difference / divisor

    return stock_linear_correlated_measure


def remove_repeated_strings(strings: list) -> list:
    unique_strings = list(set(map(str.upper, strings)))
    return unique_strings
