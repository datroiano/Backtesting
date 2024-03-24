import matplotlib.pyplot as plt


def plot_graphs(x):
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # First scatter plot: Delta Volume Percent vs Strategic Profit Percent
    x1 = x['entry_time']
    y1 = x['strategy_profit_percent']
    axs[0].scatter(x1, y1, s=10)
    axs[0].set_xlabel('Entry Time')
    axs[0].set_ylabel('Strategic Profit Percent')
    axs[0].set_title('Entry time vs profit')
    axs[0].grid(True)

    # Second scatter plot: Delta Volume Percent vs Strategic Profit Percent
    x2 = x['exit_time']
    y2 = x['strategy_profit_percent']
    axs[1].scatter(x2, y2, s=10)
    axs[1].set_xlabel('Exit Time')
    axs[1].set_ylabel('Strategic Profit Percent')
    axs[1].set_title('Exit time vs profit')
    axs[1].grid(True)

    # Third scatter plot: Stock movement vs Strategic Profit Percent
    x3 = x['stock_linear_correlated_measure']
    y3 = x['strategy_profit_percent']
    axs[2].scatter(x3, y3, s=10)
    axs[2].set_xlabel('Stock Linear Correlated Measure')
    axs[2].set_ylabel('Strategic Profit Percent')
    axs[2].set_title('Stock movement vs profit')
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
