from OptionClasses.Strategies.straddle import StraddleStrategy

nvda = StraddleStrategy(ticker='nvda',
                        strike=800,
                        expiration_date='2024-03-01',
                        quantity=1,
                        entry_date='2024-02-29',
                        exit_date='2024-02-29',
                        strategy_type='long',
                        entry_exit_period=('09:30:00', '10:00:00', '15:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        )

aapl = StraddleStrategy(ticker='aapl',
                        strike=180,
                        expiration_date='2024-03-01',
                        quantity=1,
                        entry_date='2024-02-28',
                        exit_date='2024-02-28',
                        strategy_type='long',
                        entry_exit_period=('10:30:00', '11:00:00', '14:30:00', '16:00:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        )

msft = StraddleStrategy(ticker='msft',
                        strike=405,
                        expiration_date='2024-03-01',
                        quantity=1,
                        entry_date='2024-02-28',
                        exit_date='2024-02-28',
                        strategy_type='long',
                        entry_exit_period=('09:30:00', '10:30:00', '15:00:00', '15:30:00'),
                        timespan='minute',
                        fill_gaps=True,
                        per_contract_commission=0.01,
                        multiplier=1,
                        polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                        )

crm = StraddleStrategy(ticker='crm',
                       strike=300,
                       expiration_date='2024-03-01',
                       quantity=1,
                       entry_date='2024-02-28',
                       exit_date='2024-02-28',
                       strategy_type='long',
                       entry_exit_period=('10:30:00', '13:00:00', '13:30:00', '14:00:00'),
                       timespan='minute',
                       fill_gaps=True,
                       per_contract_commission=0.01,
                       multiplier=1,
                       polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                       )

tgt_earnings = StraddleStrategy(ticker='TGT',
                                strike=150,
                                expiration_date='2024-03-08',
                                quantity=1,
                                entry_date='2024-03-05',
                                exit_date='2024-03-05',
                                strategy_type='long',
                                entry_exit_period=('10:00:00', '11:30:00', '15:00:00', '16:00:00'),
                                timespan='minute',
                                fill_gaps=True,
                                per_contract_commission=0.01,
                                multiplier=1,
                                polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                                )

jd_earnings = StraddleStrategy(ticker='jd',
                               strike=21,
                               expiration_date='2024-03-08',
                               quantity=1,
                               entry_date='2024-03-05',
                               exit_date='2024-03-05',
                               strategy_type='long',
                               entry_exit_period=('10:00:00', '11:30:00', '15:30:00', '16:00:00'),
                               timespan='minute',
                               fill_gaps=True,
                               per_contract_commission=0.01,
                               multiplier=1,
                               polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'
                               )
