

class Tx:
    def __init__(self, version, tx_ins, tx_outs,
                 locktime, _timestamp, tx_hash=None):
        self.tx_hash = tx_hash
        self.version = version
        self._timestamp = _timestamp
        self.tx_ins = tx_ins  # list
        self.tx_outs = tx_outs
        self.locktime = locktime

    def __repr__(self):
        tx_ins_s = ''
        for tx_in in self.tx_ins:
            tx_ins_s += tx_in.__repr__() + '\n'
        tx_outs_s = ''
        # for tx_out in self.tx_outs:
        tx_outs_s += self.tx_outs.__repr__() + '\n'
        return '\n tx: version: {}\n tx_ins:\n{} tx_outs:\n{} locktime: {}\n'.format(
            self.version,
            tx_ins_s,
            tx_outs_s,
            self.locktime,
        )


class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = script_sig  # (z+re)/k  ,  public key (x)  y2=x^3+7
        self.sequence = sequence

    def __repr__(self):
        return ' previous_trasaction:{}\n previous_index:{}\n script_signature: {}\n'.format(
            self.prev_tx,
            self.prev_index,
            self.script_sig
        )


class TxOut:   # utxo

    def __init__(self, amount, address, script_pubkey):
        self.amount = amount   # 5
        self.address = address  # you
        # OP_DUP OP_HASH160 your_public_key_hash OP_EQUALVERIFY OP_CHECKSIG
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return ' amount:{} BTC \n address: {}\n script_publickey:{}\n'.format(self.amount, self.address, self.script_pubkey)
