from TestCases.straddle_plays import aapl, nvda, msft, crm
from MachineLearning.conversion import clean_df
import pandas as pd

nvda_sim = nvda.run_simulation()
aapl_sim = aapl.run_simulation()
msft_sim = msft.run_simulation()
crm_sim = crm.run_simulation()

combined_sim = pd.concat([aapl_sim, nvda_sim, msft_sim, crm_sim], ignore_index=True)


learning_frame = clean_df(combined_sim)


