def calculate_sma(series, window=20):
    return series.rolling(window=window).mean()
