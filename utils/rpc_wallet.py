# utils/rpc_wallet.py

class RPCWallet:
    def __init__(self, coin):
        self.coin = coin.upper()
        self._balances = {}  # user_id -> balance

    def get_address(self, user_id):
        return f"{self.coin}_ADDR_{user_id[-6:]}"  # mock address

    def get_balance(self, user_id):
        return self._balances.get(user_id, 0.0)

    def add(self, user_id, amount):
        self._balances[user_id] = self.get_balance(user_id) + amount

    def subtract(self, user_id, amount):
        bal = self.get_balance(user_id)
        if amount > bal:
            raise Exception("Insufficient funds")
        self._balances[user_id] = bal - amount

    def send(self, sender_id, receiver_id, amount):
        self.subtract(sender_id, amount)
        self.add(receiver_id, amount)

    def withdraw(self, user_id, address, amount):
        self.subtract(user_id, amount)
        return f"{self.coin}_TXID_{user_id[-6:]}"
