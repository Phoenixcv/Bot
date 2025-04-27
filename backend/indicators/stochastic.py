def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    low_min = low.rolling(window=k_period).min()
    high_max = high.rolling(window=k_period).max()
    k = 100 * ((close - low_min) / (high_max - low_min))
    d = k.rolling(window=d_period).mean()
    return k.iloc[-1], d.iloc[-1]
