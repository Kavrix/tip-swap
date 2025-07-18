# utils/rate.py

EXCHANGE_RATES = {
    ('DOGE', 'AUS'): 0.75,
    ('AUS', 'DOGE'): 1.33,
    ('DOGE', 'DINGO'): 2.0,
    ('DINGO', 'DOGE'): 0.5,
    ('AUS', 'DINGO'): 2.5,
    ('DINGO', 'AUS'): 0.4,
    # Add all other pairings
}

def get_rate(from_coin: str, to_coin: str) -> float:
    """Get fixed exchange rate between two coins"""
    if from_coin == to_coin:
        return 1.0  # No conversion
    rate = EXCHANGE_RATES.get((from_coin.upper(), to_coin.upper()))
    if rate is None:
        raise ValueError(f"No rate defined for {from_coin} -> {to_coin}")
    return rate

def convert(amount: float, from_coin: str, to_coin: str) -> float:
    """Convert amount using fixed rates"""
    rate = get_rate(from_coin, to_coin)
    return round(amount * rate, 8)
