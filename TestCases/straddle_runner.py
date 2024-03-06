from TestCases.straddle_plays import aapl, nvda, msft, crm, tgt_earnings, jd_earnings
from MachineLearning.conversion import clean_df
import pandas as pd

nvda_sim = nvda.run_simulation()
aapl_sim = aapl.run_simulation()
msft_sim = msft.run_simulation()
crm_sim = crm.run_simulation()
tgt_earnings_sim = tgt_earnings.run_simulation()
jd_earnings_sim = jd_earnings.run_simulation()

combined = False
earnings_combined = True
combined_sim = pd.concat([aapl_sim, nvda_sim, msft_sim, crm_sim], ignore_index=True)
earnings_combined_sim = pd.concat([tgt_earnings_sim, jd_earnings_sim], ignore_index=True)

if earnings_combined:
    learning_frame = clean_df(earnings_combined_sim)
else:
    learning_frame = clean_df(combined_sim) if combined else clean_df(jd_earnings_sim)


