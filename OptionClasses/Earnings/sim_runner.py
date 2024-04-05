from OptionClasses.Earnings.company_tickers import sim_tickers_1, sim_tickers_2, sim_tickers_3
from OptionClasses.Earnings.lookup import StrategyTestInputs
from datetime import datetime

used_sim = sim_tickers_3

current_date = datetime.now()
formatted_date = current_date.strftime('%Y-%m-%d')

reference_date = formatted_date

x = StrategyTestInputs(used_sim,
                       entry_exit_period=('10:30:00', '11:30:00', '15:30:00', '16:00:00'),
                       lookup_period_months=5,
                       lookup_from=reference_date)

sims = x.aggregate_ticker_simulations()
errors = x.errors_list
tested = x.tested_tickers
