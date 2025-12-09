import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def overview(ohlc_data, strategy_position, capital_list, drawdown_list, market_return=[]):

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)

    # Plot the first chart
    plot_chart(ax1, ohlc_data, strategy_position)

    # Plot the second chart for overview
    plot_overview(ax2, capital_list, drawdown_list, market_return)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the figure with both subplots
    plt.show()

def plot_chart(ax, data, signal):
    # Extract OHLC data from the input
    dates = data[0]
    opens = data[1]
    highs = data[2]
    lows = data[3]
    closes = data[4]

    # Create a DataFrame with OHLC data
    df = pd.DataFrame({
        'date': dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes
    })
    x = np.arange(len(closes))

    # Define the width of candlestick elements
    width = 0.8
    width2 = 0.2

    color = ["green" if close_price > open_price else "red" for close_price, open_price in zip(df.close, df.open)]
    ax.bar(x=x, height=np.abs(df.open-df.close), bottom=np.min((df.open,df.close), axis=0), width=width, color=color)
    ax.bar(x=x, height=df.high-df.low, bottom=df.low, width=width2, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)

    # Plot markers based on signals
    buy = np.where(np.any(signal == 1, axis=1))[0]
    sell = np.where(np.any(signal == -1, axis=1))[0]
    exit = np.where(np.any(signal == 0, axis=1))[0]

    ax.plot(x[buy], closes[buy], marker='^', markersize=8, color='b', linestyle='None')
    ax.plot(x[sell], closes[sell], marker='v', markersize=8, color='m', linestyle='None')
    ax.plot(x[exit], closes[exit], marker='x', markersize=8, color='k', linestyle='None')

    ax.set_ylabel("Price")
    ax.set_title("Chart")

def plot_overview(ax, capital_list, drawdown_list, market_return=[]):
    drawdown_percentage_list = drawdown_list

    twin1 = ax.twinx()

    # Plot capital and drawdown
    p1, = ax.plot(np.arange(0, len(capital_list)), capital_list, "dodgerblue")
    ax.fill_between(np.arange(0, len(capital_list)), 0, capital_list, color='dodgerblue', alpha=0.7)
    p2, = twin1.plot(np.arange(0, len(capital_list)), drawdown_percentage_list, "orangered")
    twin1.fill_between(np.arange(0, len(capital_list)), 0, drawdown_percentage_list, color='orangered', alpha=0.7)

    if len(market_return) > 0:
        # Plot market return if available
        p3, = ax.plot(np.arange(0, len(market_return)), market_return, "black")

    ax.set_xlim(0, len(capital_list)-1)
    ax.set_ylim(0, max(capital_list))
    twin1.set_ylim(-100, 0)

    ax.set_xlabel("Trades")
    ax.set_ylabel("Profit")
    twin1.set_ylabel("Drawdown %")

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())

    ax.tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())

    ax.tick_params(axis='x')