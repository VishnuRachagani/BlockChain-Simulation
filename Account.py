class MyAccount:  # wallet
    def __init__(self, private, public, bitcoinAddress, utxo, balance):
        self.private = private
        self.public = public  # public key object # S256Point -> fun verify()
        self.bicoinAddress = bitcoinAddress
        self.utxo = utxo  # list of TXOut
        self.total_balance = balance
        # self._balance()

    def _balance(self):
        amount = 0
        if self.utxo != None:
            for p in self.utxo:
                amount += p.amount

        self.total_balance = amount
        return self.total_balance
