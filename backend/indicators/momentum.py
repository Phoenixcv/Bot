def calculate_momentum(prices: list, period: int = 10):
    if len(prices) < period + 1:
        return None
    return prices[-1] - prices[-(period + 1)]
