from TestCases.straddle_plays import earnings_combined
from MachineLearning.conversion import clean_df, filter_stock_basis
from Jupyter.jupyter_app import visualize_and_correlate

x = filter_stock_basis(earnings_combined, movement_maximum=0.01)
