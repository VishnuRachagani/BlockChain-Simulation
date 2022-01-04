from Account import MyAccount
from ecc import PublicKey, Signature
from helper import hash256, hash160, encode_base58_checksum, decode_base58
from helper import merkle_root, merkle_parent_level, merkle_parent
from block import Block
from datetime import datetime
from tx import Tx, TxIn, TxOut
import random
seed = 'hello world'  # seed used for generating the private keys
private_keys = []
public_keys = []
public_key_hashes = []
bitcoin_addresses = []
my_accounts = {}
current_transactions = []  # transaction objects (Tx objects)
current_transactions_hashes = []  # transaction id's hash(tx_int+tx_out)
# s256fields = []
for i in range(10):
    private_keys.append(hash256((seed+str(i)).encode('utf-8')).hex())
print('Private Keys')
for i in range(10):

    print('[{}] {}'.format(i, private_keys[i]))


# generating public keys from private keys
for i in range(10):
    key1 = PublicKey(int('0x'+private_keys[i], 16))
    # s256fields.append(key1.point)
    public_keys.append(key1)
    # hash 256 followed by ripemd
    _hash = hash160(
        (str(key1.point.x)+str(key1.point.y)).encode('utf-8')).hex()
    public_key_hashes.append(_hash)
    _hash = '00'+_hash
    _hash = encode_base58_checksum(bytes.fromhex(_hash))

    # print(_hash)

    bitcoin_addresses.append(_hash)

    # account1=MyAccount()
    # account2=MyAccount()
    # account3=MyAccount()


# adding eveything into accounts
for i in range(10):
    account1 = MyAccount(
        private_keys[i], public_keys[i], bitcoin_addresses[i], [], 0)
    my_accounts[bitcoin_addresses[i]] = account1
    print(bitcoin_addresses[i])

# print("Enter amount to send")
# amount=input()


# creating the coin base transaction


blockchain = []
_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
# script__public__key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
# bitcoin_addresses[0])

t_input = TxIn(prev_tx='COINBASE (Newly Generated Coins)', prev_index=0,
               script_sig=None, sequence=0xffffffff)
script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
    public_key_hashes[0])
t_out = TxOut(50, bitcoin_addresses[0], script_public_key)
t__input = [t_input]
genesis_transaction = Tx(1, t__input, t_out, 0,
                         datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

transaction_id = hash256(repr(genesis_transaction).encode('utf-8')).hex()
# print(transaction_id)
genesis_transaction.tx_hash = transaction_id

# genesis block
genesis_block = Block(version=1, prev_block=str(0x00000000000000000000000000000000), merkle_root=None,
                      timestamp=_time, nonce=0, tx_hashes=[transaction_id], tx_objects=[genesis_transaction])
merkle__root = merkle_root([transaction_id])
genesis_block.merkle_root = merkle__root
my_accounts[genesis_transaction.tx_outs.address].utxo = [
    genesis_transaction.tx_outs]
genesis_block.block_hash = str(genesis_block.hash())  # block hash
blockchain.append(genesis_block)  # adding to the block chain


def _create_coinbase_transaction(_miner):
    _time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    t_input = TxIn(prev_tx='COINBASE (Newly Generated Coins)', prev_index=0,
                   script_sig=None, sequence=0xffffffff)
    script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
        bitcoin_addresses[_miner])
    t_out = TxOut(50, bitcoin_addresses[_miner], script_public_key)
    t__input = [t_input]
    #t__out = [[t_out]]
    coinbase_transaction = Tx(1, t__input, t_out, 0,
                              datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    transaction_id = hash256(repr(coinbase_transaction).encode(
        'utf-8')).hex()  # sha256  2 times
    # print(transaction_id)
    #Tx . tx_hash
    coinbase_transaction.tx_hash = transaction_id
    my_accounts[bitcoin_addresses[_miner]].utxo.append(
        coinbase_transaction.tx_outs)
    return coinbase_transaction


# verifying the transaction using elliptic curve cryptography

def _verify_transactions():
    start = 0
    # Tx object
    for __x in current_transactions:
        my_hash = current_transactions_hashes[start]
        start = start+1
        # [Tx(prev_out),Tx(),Tx()]
        # iterating tx_in list
        for __p in __x.tx_ins:
            signature = Signature.parse(__p.script_sig)  # (r,s)
            # wallet map
            # key -> value   === bitcoint_address -> MyAccount object
            # TXout (amount, address, script public key) (UTXO)a --->   #b
            if (my_accounts[__p.prev_tx.address].public.point.verify(
                    int('0x'+my_hash, 16), signature)) == False:  # removing the transactions those are failed
                current_transactions.remove(__x)
                # current_transactions_hashes

    # for tran_obs in current_transactions:


def _create_block(tx_hashes, my_tx_objects):
    target = random.getrandbits(256)
    _block = None
    _miner = random.randint(0, 9)

    if (len(my_tx_objects) == 0):
        return
    print("mining")
    print('curremt miner is :')
    print(bitcoin_addresses[_miner])
    prev_block = blockchain[-1].block_hash
    # tx objects
    _objects = my_tx_objects.copy()
    __hashes = tx_hashes.copy()
    _objects.append(_create_coinbase_transaction(_miner))
    __hashes.append(_objects[-1].tx_hash)
    # remove bits
    _time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    _block = Block(version=1, prev_block=prev_block, merkle_root=merkle_root(tx_hashes),
                   timestamp=_time, nonce=0, tx_hashes=__hashes, tx_objects=_objects)
    temp_block_hash = None
    # mining
    while(True):
        _block.nonce += 1
        temp_block_hash = _block.hash()
        if(int(temp_block_hash, 16) <= target or _block.nonce > 10000):
            break

    # print(_block.nonce)
    _block.block_hash = str(temp_block_hash)
    # list of Tx (tx_ins,tx_outs) #tx_outs for receiver
    for __x in my_tx_objects:
        amount = 0
        for __input in __x.tx_ins:
            amount += __input.prev_tx.amount
       # amount 9
        # for __y in __x.tx_outs:
        #print('hello j')
        # print(__x[].tx_outs)
        my_accounts[__x.tx_outs.address].utxo.append(
            __x.tx_outs)
        # amount 9-7=2
        amount -= __x.tx_outs.amount
        if amount > 0:
            script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
                __x.tx_ins[0].prev_tx.address)
            # tx_ins  is list of tx_in(prev_tx) prev_tx is Txout

            my_accounts[__x.tx_ins[0].prev_tx.address].utxo.append(
                TxOut(amount, __x.tx_ins[0].prev_tx.address, script_public_key))

    current_transactions_hashes.clear()
    current_transactions.clear()
    blockchain.append(_block)


# print(my_accounts[bitcoin_addresses[0]]._balance())


# creating the user transaction

  
def create_and_send(_a, _b, _amount):
    # bitcoin address  ->  myaccount object
    if my_accounts[bitcoin_addresses[_a]]._balance() < _amount:
        print('failed to create transaction')
        return
    else:
        print('creating')
        # utxo list Txout objects
        _utxo = my_accounts[bitcoin_addresses[_a]].utxo
        picked_utxo = []
        my_amount = 0
        for x in _utxo:
            my_amount += x.amount
            picked_utxo.append(x)
            _utxo.remove(x)
            if my_amount >= _amount:
                break

        my_accounts[bitcoin_addresses[_a]].utxo = _utxo
        script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
            public_key_hashes[_b])
        # script__public__key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
        #     bitcoin_addresses[_a])

        t_input = []
        t_out = None
        for _x in picked_utxo:
            t_input.append(TxIn(prev_tx=_x, prev_index=0,
                           script_sig=None, sequence=0xffffffff))

        t_out = TxOut(_amount, bitcoin_addresses[_b], script_public_key)
        # t__input = t_input
        # t__out = t_out
        my_transaction = Tx(1, t_input, t_out, 0,
                            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        transaction_id = hash256(
            repr(my_transaction).encode('utf-8')).hex()
        for __input in my_transaction.tx_ins:  # list of transaction inputs
            __input.script_sig = public_keys[_a].sign(
                int('0x'+transaction_id, 16)).der()

        my_transaction.tx_hash = transaction_id
        current_transactions_hashes.append(transaction_id)
        # list of transaction objects
        current_transactions.append(my_transaction)

# verify the transactions and creating the block


def start__():
    _verify_transactions()
    _create_block(current_transactions_hashes, current_transactions)



create_and_send(0, 1, 10)
start__()


create_and_send(0, 3, 20)
start__()

create_and_send(0, 3, 1)
start__()

create_and_send(0, 7, 2)
start__()

create_and_send(0, 6, 2)
start__()

create_and_send(0, 5, 2)
start__()

create_and_send(0, 8, 2)
start__()

create_and_send(0, 3, 2)
start__()

create_and_send(0, 9, 2)
start__()

# print(my_accounts[bitcoin_addresses[1]]._balance())
# print(my_accounts[bitcoin_addresses[0]]._balance())
# print(my_accounts[bitcoin_addresses[3]]._balance())
print("            Address           :     Money")
for i in range(10):

    print("{} : {} BTC".format(
        bitcoin_addresses[i], my_accounts[bitcoin_addresses[i]]._balance()))

for i in range(len(blockchain)):
    print('block:{}\n'.format(i))
    print(blockchain[i])
