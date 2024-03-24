from OptionClasses.Strategies.straddle import StraddleStrategy
import pandas as pd

entry_time1 = '11:30:00'
entry_time2 = '12:45:00'
exit_time1 = '15:00:00'
exit_time2 = '16:00:00'

# PRE-EARNINGS LONG STRADDLES (TEST CASE)


aapl = StraddleStrategy(ticker='AAPL',
                        strike=187.5,
                        expiration_date='2024-02-02',
                        quantity=1,
                        entry_date='2024-02-01',
                        exit_date='2024-02-01',
                        strategy_type='long',
                        entry_exit_period=(entry_time1, entry_time2, exit_time1, exit_time2),
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
                        entry_exit_period=(entry_time1, entry_time2, exit_time1, exit_time2),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

acn = StraddleStrategy(ticker='ACN',  # RAN
                       strike=380,
                       expiration_date='2024-03-22',
                       quantity=1,
                       entry_date='2024-03-20',
                       exit_date='2024-03-20',
                       strategy_type='long',
                       entry_exit_period=(entry_time1, entry_time2, exit_time1, exit_time2),
                       timespan='minute',
                       fill_gaps=True,
                       per_contract_commission=0.01,
                       multiplier=1,
                       polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

adbe = StraddleStrategy(ticker='adbe',
                        strike=570,
                        expiration_date='2024-03-15',
                        quantity=1,
                        entry_date='2024-03-14',
                        exit_date='2024-03-14',
                        strategy_type='long',
                        entry_exit_period=(entry_time1, entry_time2, exit_time1, exit_time2),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

nke = StraddleStrategy(ticker='NKE',
                       strike=100,
                       expiration_date='2024-03-22',
                       quantity=1,
                       entry_date='2024-03-21',
                       exit_date='2024-03-21',
                       strategy_type='long',
                       entry_exit_period=(entry_time1, entry_time2, exit_time1, exit_time2),
                       timespan='minute',
                       fill_gaps=True,
                       per_contract_commission=0.01,
                       multiplier=1,
                       polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

nke_sim = nke.run_simulation()
aapl_sim = aapl.run_simulation()
msft_sim = msft.run_simulation()
acn_sim = acn.run_simulation()
adbe_sim = adbe.run_simulation()

earnings_combined = pd.concat([nke_sim, aapl_sim, msft_sim, acn_sim, adbe_sim], ignore_index=True)
