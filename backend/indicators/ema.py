def calculate_ema(series, span=20):
    return series.ewm(span=span, adjust=False).mean()
