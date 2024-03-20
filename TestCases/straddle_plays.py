from OptionClasses.Strategies.straddle import StraddleStrategy
import pandas as pd


# NON-EARNINGS LONG STRADDLES (CONTROL)
nvda = StraddleStrategy(ticker='NVDA',
                        strike=887.5,
                        expiration_date='2024-03-22',
                        quantity=1,
                        entry_date='2024-03-19',
                        exit_date='2024-03-19',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

aapl = StraddleStrategy(ticker='AAPL',
                        strike=177.5,
                        expiration_date='2024-03-22',
                        quantity=1,
                        entry_date='2024-03-19',
                        exit_date='2024-03-19',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

msft = StraddleStrategy(ticker='MSFT',
                        strike=422.5,
                        expiration_date='2024-03-22',
                        quantity=1,
                        entry_date='2024-03-19',
                        exit_date='2024-03-19',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

nvda_sim = nvda.run_simulation()
aapl_sim = aapl.run_simulation()
msft_sim = msft.run_simulation()

non_earnings_combined = pd.concat([msft_sim, aapl_sim, nvda_sim], ignore_index=True)

# PRE-EARNINGS LONG STRADDLES (TEST CASE)

nvda = StraddleStrategy(ticker='NVDA',
                        strike=675,
                        expiration_date='2024-02-23',
                        quantity=1,
                        entry_date='2024-02-21',
                        exit_date='2024-02-21',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

aapl = StraddleStrategy(ticker='AAPL',
                        strike=187.5,
                        expiration_date='2024-02-02',
                        quantity=1,
                        entry_date='2024-02-01',
                        exit_date='2024-02-01',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

msft = StraddleStrategy(ticker='MSFT',
                        strike=410,
                        expiration_date='2024-02-02',
                        quantity=1,
                        entry_date='2024-01-30',
                        exit_date='2024-01-30',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:45:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

nvda_sim = nvda.run_simulation()
aapl_sim = aapl.run_simulation()
msft_sim = msft.run_simulation()

earnings_combined = pd.concat([msft_sim, aapl_sim, nvda_sim], ignore_index=True)
print(StraddleStrategy.get_meta_data(nvda_sim))
print(StraddleStrategy.get_meta_data(aapl_sim))
print(StraddleStrategy.get_meta_data(msft_sim))