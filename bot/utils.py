def format_balance(balances):
    """Format balances dict into a user-readable string."""
    return "\n".join([f"{coin}: {amount:.8f}" for coin, amount in balances.items()])
