from OptionClasses.Strategies.straddle import StraddleStrategy
from MachineLearning.conversion import clean_df


test = StraddleStrategy(ticker='nvda',
                        strike=790,
                        expiration_date='2024-03-01',
                        quantity=1,
                        entry_date='2024-02-29',
                        exit_date='2024-02-29',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:30:00', '12:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        )

learning_frame = clean_df(test.run_simulation())
