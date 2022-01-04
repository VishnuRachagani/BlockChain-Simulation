from helper import (
    hash256,
)


class Block:

    def __init__(self, version, prev_block=0x00000000000000000000000000000000, merkle_root=None,
                 timestamp=None, nonce=0, tx_hashes=None, tx_objects=None, block_hash=None):
        self.block_hash = block_hash
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nonce = nonce
        self.tx_hashes = tx_hashes
        self.tx_objects = tx_objects

    def __repr__(self):
        transactions = ''
        for tx in self.tx_objects:
            transactions += tx.__repr__()+'\n'

        return ' block_hash: {}\n previous_block: {}\n merkle_root: {} \n timestamp: {}\n nonce: {} \n transactions: {}\n'.format(
            self.block_hash,
            self.prev_block,
            self.merkle_root,
            self.timestamp,
            self.nonce,
            transactions
        )

    def hash(self):
        s = str(self.prev_block[::-1])+str(self.merkle_root[::-1]) + \
            str(self.version)+str(self.timestamp)+str(self.nonce)
        h256 = hash256(s.encode('utf-8'))
        return h256[::-1].hex()
