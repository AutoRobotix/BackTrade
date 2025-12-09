# BackTrade

BackTrade provides a robust Python module for conducting professional **backtests** of trading strategies using historical OHLCV (Open, High, Low, Close, Volume) data and for **visualizing** the resulting performance metrics.

-----

## 🛠️ Modules and Dependencies

The core functionality relies on standard scientific and financial Python libraries:

  * **`numpy`**: Essential for efficient array manipulation and complex mathematical operations, such as Drawdown calculation.
  * **`decimal`**: Ensures high precision in financial calculations, crucial for accurate P\&L tracking.
  * **`math`**: Used for standard mathematical functions.
  * **`matplotlib`**: Provides the foundation for generating professional-grade financial charts.
  * **`pandas`**: Utilized within the graphics module for data structuring and visualization preparation.

You can install the necessary dependencies using pip:

```bash
pip install numpy pandas matplotlib
pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git
```

-----

## ⚙️ Backtesting Engine

The backtesting engine features two primary functions, both designed to simulate trade execution across historical data, accounting for various market costs.

### `backtest(ohlc_data, info, strategy_position, leverage=1, margin=100, capital=1000)`

This function executes a **comprehensive backtest**. It simulates trading mechanics including **spread**, **leverage**, and **overnight financing fees** (long/short).

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `ohlc_data` | `list` of `np.array` | Historical OHLCV data structure: `[date, open, high, low, close, volume]`. |
| `info` | `dict` | Ticker-specific parameters: `{'precision': float/int, 'spread': float, 'long_overnight': float, 'short_overnight': float}`. |
| `strategy_position` | `np.array` (2D) | Strategy signals array for each **bar** and each concurrent **call** (column): `1` (Long), `-1` (Short), `0` (Exit/Flat). |
| `leverage` | `int` | The leverage multiplier to apply (Default: 1). |
| `margin` | `int` | Percentage of capital allocated per trade call (Default: 100). |
| `capital` | `float` | Initial starting capital (Default: 1000). |

#### Returns

  * `capital_list`: A list of capital values after each closed trade.
  * `dd_list`: A corresponding list of maximum Drawdown percentages.

### `backmarket(ohlc_data, info, strategy_position, margin=100, capital=1000)`

This function performs a **Market Risk-Adjusted backtest**. It is a simplified version that excludes leverage and overnight fees, focusing primarily on the **market return** based on the entry/exit signals.

#### Returns

  * `capital_list`: A list of capital values after each closed trade.

-----

## 📊 Visualization Module (`graphics`)

The `graphics` module provides tools to professionally present the backtesting results.

### `overview(ohlc_data, strategy_position, capital_list, drawdown_list, market_return=[])`

The main visualization function generates a figure with two subplots:

1.  **Trading Chart (`plot_chart`):** Displays the **candlestick chart** (`OHLC`) with visual markers for strategy signals:
      * **Buy/Long Entry:** `^` (Blue triangle)
      * **Sell/Short Entry:** `v` (Magenta triangle)
      * **Position Exit/Flat:** `x` (Black cross)
2.  **Performance Overview (`plot_overview`):** Displays key performance metrics over the trade sequence:
      * **Capital/Profit** (Area plot, Blue)
      * **Drawdown Percentage** (Secondary axis, Orange-Red)
      * **Market Return** (Optional line plot, Black)

This combined view allows for an immediate correlation between strategy signals and equity curve performance.