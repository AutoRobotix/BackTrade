import numpy as np
import decimal
import math

### ---     BACKTESTER     --- ###
###  MAIN LOOP  ###
def backtest(ohlc_data, info, strategy_position, leverage: int = 1, margin=100, capital=1000):
    """
    - ohlc_data: list of arrays with OHLCV data [date, open, high, low, close, volume]
    - info: dictionary with ticker info (precision, spread, long/shortovernight fees)
    - strategy_position: 2D array with strategy positions for each call
    - leverage: leverage multiplier (default: 1)
    - margin: percentage of capital to use for margin (default: 100)
    - capital: initial capital for backtesting (default: 1000)

    Returns:
    - capital_list: list of capital values after each closed trade
    - dd_list: list of drawdown percentages corresponding to capital_list
    """

    # Ticker info
    precision = info['precision']
    if precision == int(precision):
        precision = int(precision)
    spread = info['spread']
    long_overnight = info['long_overnight']
    short_overnight = info['short_overnight']

    # OHLC data
    date  = ohlc_data[0]
    #open = ohlc_data[1]
    #high = ohlc_data[2]
    #low  = ohlc_data[3]
    close = ohlc_data[4]
    #volume = ohlc_data[5]

    # Variables
    profit = 0
    overnight_fees = 0
    margin = margin /100
    calls = len(strategy_position[0])

    entry_price = [np.nan for _ in range(0, calls)]
    entry_date = [np.nan for _ in range(0, calls)]
    last_position = [0 for _ in range(0, calls)]
    shares = [0 for _ in range(0, calls)]

    # Output lists
    capital_list = [capital]
    dd_list = [0]

    ### ---  BACKTEST LOOP  --- ###
    for index in range(1, len(strategy_position)): 
        for call in range(0, calls):

            # --- EXITS AND CALCULATIONS 

                # LONG EXIT
                if (strategy_position[index-1][call] <= 0) and (last_position[call] > 0):   
                    exit_price = close[index-1] #open[index]  
                    exit_date = date[index].date()
           
                    # Profit calculation
                    if leverage > 1: 
                        overnight_fees = ((shares[call] * exit_price) * (long_overnight / 100)) * ((exit_date-entry_date[call]).days) 
                    else:
                        overnight_fees = 0
                    profit += ((exit_price - entry_price[call]) * shares[call]) - overnight_fees

                    # Reset call
                    entry_price[call] = np.nan
                    entry_date[call] = np.nan
                    last_position[call] = 0
                    shares[call] = 0

                # SHORT EXIT 
                elif (strategy_position[index-1][call] >= 0) and (last_position[call] < 0): 
                    exit_price = close[index-1] #open[index]  
                    exit_date = date[index].date()
          
                    # Profit calculation
                    if leverage > 1: 
                        overnight_fees = (shares[call] * exit_price) * (short_overnight / 100) * ((exit_date-entry_date[call]).days) 
                    else:
                        overnight_fees = 0        
                    profit += ((entry_price[call] - exit_price) * shares[call]) - overnight_fees

                    # Reset call
                    entry_price[call] = np.nan
                    entry_date[call] = np.nan
                    last_position[call] = 0
                    shares[call] = 0

            # --- ENTRIES

                # LONG ENTRY
                if (strategy_position[index-1][call] > 0) and (last_position[call] <= 0): 
                    amount = (capital*margin)/calls
                    entry_price[call] = close[index-1] + spread # open[index] + spread 
                    entry_date[call] = date[index].date() 
                    shares[call] = float(decimal.Decimal(amount/entry_price[call]).quantize(decimal.Decimal(str(precision)))) * leverage
                    last_position[call] = 1

                # SHORT ENTRY
                elif (strategy_position[index-1][call] < 0) and (last_position[call] >= 0):
                    amount = (capital*margin)/calls
                    entry_price[call] = close[index-1] - spread # open[index] - spread 
                    entry_date[call] = date[index].date()  
                    shares[call] = float(decimal.Decimal(amount/entry_price[call]).quantize(decimal.Decimal(str(precision)))) * leverage
                    last_position[call] = -1

        if profit != 0:
            capital = math.floor((capital + profit)*100)/100
            capital_list.append(capital)
            profit = 0
            if capital <= 10:
                break  

    ###  OUTPUT  ###
    dd_list = -(100 * (np.maximum.accumulate(np.array(capital_list)) - np.array(capital_list)) / np.maximum.accumulate(np.array(capital_list))) 
    return capital_list, dd_list
     

     
def backmarket(ohlc_data, info, strategy_position, margin=100, capital=1000):
    """
    Market risk-adjusted backtester 

    - ohlc_data: list of arrays with OHLCV data [date, open, high, low, close, volume]
    - info: dictionary with ticker info (precision, spread, long/shortovernight fees)
    - strategy_position: 2D array with strategy positions for each call
    - margin: percentage of capital to use for margin (default: 100)
    - capital: initial capital for backtesting (default: 1000)

    Returns:
    - capital_list: list of capital values after each closed trade
    """

    # Ticker info & close prices
    precision = info['precision']
    if precision == int(precision):
        precision = int(precision)
    spread = info['spread']
    close  = ohlc_data[4]

    # Variables
    profit = 0
    margin = margin /100
    calls = len(strategy_position[0])
    entry_price = [np.nan for _ in range(0, calls)]
    last_position = [0 for _ in range(0, calls)]
    shares = [0 for _ in range(0, calls)]

    # Output list
    capital_list = [capital]

    # FIRST BAR 
    strategy_position[0, 0] = 1
    strategy_position[1:-2, 0] = np.nan
    strategy_position[-2, 0] = 0

    ### ---  BACKTEST LOOP  --- ###
    for index in range(1, len(strategy_position)): 
        for call in range(0, calls):

                #####  EXITS AND CALCULATIONS  #####

                # LONG EXIT
                if (strategy_position[index-1][call] <= 0) and (last_position[call] > 0):   
                    exit_price = close[index-1] #open[index]             
                    profit += ((exit_price - entry_price[call]) * shares[call]) 

                    # Reset call
                    entry_price[call] = np.nan
                    last_position[call] = 0
                    shares[call] = 0

                # SHORT EXIT 
                elif (strategy_position[index-1][call] >= 0) and (last_position[call] < 0): 
                    exit_price = close[index-1] #open[index]  
                    profit += ((entry_price[call] - exit_price) * shares[call]) 

                    # Reset call
                    entry_price[call] = np.nan
                    last_position[call] = 0
                    shares[call] = 0

                #####  ENTRIES  #####

                # LONG ENTRY
                if (strategy_position[index-1][call] > 0) and (last_position[call] <= 0): 
                    amount = (capital*margin)/calls
                    entry_price[call] = close[index-1] + spread # open[index] + spread 
                    shares[call] = float(decimal.Decimal(amount/entry_price[call]).quantize(decimal.Decimal(str(precision))))
                    last_position[call] = 1

                # SHORT ENTRY
                elif (strategy_position[index-1][call] < 0) and (last_position[call] >= 0):
                    amount = (capital*margin)/calls
                    entry_price[call] = close[index-1] - spread # open[index] - spread 
                    shares[call] = float(decimal.Decimal(amount/entry_price[call]).quantize(decimal.Decimal(str(precision))))
                    last_position[call] = -1

        if profit != 0:
            capital = math.floor((capital + profit)*100)/100
            capital_list.append(capital)
            profit = 0
            if capital <= 10:
                break 

    ###  OUTPUT  ###
    return capital_list