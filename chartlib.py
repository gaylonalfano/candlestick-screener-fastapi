import os
import pandas as pd

def is_consolidating(df: pd.DataFrame, range_percentage: float = 2.0) -> bool:
    # 1. Grab recent candlesticks
    recent_candlesticks = df.iloc[-15:]
    # print(recent_candlesticks)

    # 2. Compute the max/min closes from recent_candlesticks
    max_close = recent_candlesticks["Close"].max()
    min_close = recent_candlesticks["Close"].min()
    # print("max_close:", max_close)
    # print("min_close:", min_close)

    # 3. Define a consolidation range percentage
    # NOTE We want those with min_close is really close to max_close
    # range_threshold = (100 - range_percentage) / 100  # .98 Works
    range_threshold = 1 - (range_percentage / 100)  # .98 Works
    # print(max_close * range_threshold)
    # print(f"{min_close} > {max_close * range_threshold}?  {min_close > (max_close * range_threshold)}")
    if min_close > (max_close * range_threshold):
        # print(recent_candlesticks)
        return True

    return False



def is_breaking_out(df: pd.DataFrame, range_percentage: float = 2.5) -> bool:
    """
    Computes whether last candle is breaking out when previously
    (second-to-last candle) it was consolidating.
    """
    # 1. Grab the last close value
    # NOTE Experimenting with various retreiving data methods
    # last_close_loc = df.loc[-1:, "Close"].values[0]  # Wrong! Gets FIRST row...
    # print("last_close loc", last_close_loc)
    # last_close_slice = df[-1:]["Close"].values[0]  # Works
    # print("last_close []", last_close_slice)
    # last_close_iloc = df.iloc[-1:]["Close"].values[0]  # Works
    # last_close_iloc = df.iloc[-1:, "Close"].values[0]  # Error
    last_close_iloc = df.iloc[-1:, 5].values[0]  # Works
    # print("last_close iloc", last_close_iloc)
    # second_to_last_close_iloc = df.iloc[-2:-1, 5].values[0]
    # print("second_to_last_close_iloc", second_to_last_close_iloc)  # Works
    # second_to_last_close_iloc = df.iloc[-2:-1, 5].values[0]
    # print("second_to_last_close_iloc", second_to_last_close_iloc)  # Works

    # 2. Compute whether the previous group of candlesticks is consolidating
    # NOTE We use our helper function but EXCLUDE last_close record/index
    if is_consolidating(df.iloc[:-1], range_percentage=range_percentage):
        # 2.1 Determine whether last_close is gt max of consolidating set
        recent_candlesticks = df.iloc[-16:-1]
        max_close = recent_candlesticks["Close"].max()

        if last_close_iloc > max_close:
            return True

        return False


for filename in os.listdir("datasets/daily"):
    # print(filename)
    df = pd.read_csv(f"datasets/daily/{filename}")
    # print(f"iloc[-15:] for {filename}\n", df.iloc[-15:])


    if is_consolidating(df, range_percentage=2.5):
        print(f"{filename} is consolidating")


    if is_breaking_out(df):
        print(f"{filename} is breaking out")
