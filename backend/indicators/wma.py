def calculate_wma(series, window=20):
    weights = range(1, window + 1)
    return series.rolling(window).apply(lambda prices: sum(weights * prices) / sum(weights), raw=True)
