from bitcoinrpc.authproxy import AuthServiceProxy

class RPCWallet:
    def __init__(self, rpc_url):
        self.rpc = AuthServiceProxy(rpc_url)

    def get_balance(self, address=None):
        return self.rpc.getbalance(address) if address else self.rpc.getbalance()

    def get_new_address(self):
        return self.rpc.getnewaddress()

    def send_to_address(self, address, amount):
        return self.rpc.sendtoaddress(address, amount)
