from tvDatafeed import TvDatafeed, Interval
from graphics import overview
import BackTest
import numpy as np

# Download and format historical data
tv = TvDatafeed()
ohlc_data = tv.get_hist(symbol='AAPL', exchange='NASDAQ', interval=Interval.in_daily, n_bars=1000)
ohlc_data = [ohlc_data.index,
             ohlc_data['open'].values,
             ohlc_data['high'].values,
             ohlc_data['low'].values,
             ohlc_data['close'].values,
             ohlc_data['volume'].values]

# Random ticker info
ticker_info = {
    'precision': 2,
    'spread': 0.01*ohlc_data[1][0],
    'long_overnight': 0.01,
    'short_overnight': 0.01}

# Random strategy positions for testing
strategy_position = np.array([np.array([np.nan]) for _ in range(len(ohlc_data[0]))])
strategy_position[0][0] = 1 
strategy_position[400][0] = 0
strategy_position[600][0] = 1  
strategy_position[-2][0] = 0  

# Run backtest & plot results
capital_list, drawdown_list = BackTest.backtest(ohlc_data, ticker_info, strategy_position)
market_return = BackTest.backmarket(ohlc_data, ticker_info, strategy_position)

overview(ohlc_data, strategy_position, capital_list, drawdown_list, market_return)