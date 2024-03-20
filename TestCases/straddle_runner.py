from TestCases.straddle_plays import non_earnings_combined, earnings_combined
from MachineLearning.conversion import clean_df
from Jupyter.jupyter_app import visualize_and_correlate

visualize_and_correlate(clean_df(earnings_combined))
visualize_and_correlate(clean_df(non_earnings_combined))
